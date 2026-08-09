function result = verifyEeglabBids( ...
    eeglabRoot, bidsRoot, subjectLabel, taskLabel, runLabel, options)
%VERIFYEEGLABBIDS Exercise one explicit EEG-BIDS selection outside its source.

arguments
    eeglabRoot (1, 1) string {mustBeFolder}
    bidsRoot (1, 1) string {mustBeFolder}
    subjectLabel (1, 1) string
    taskLabel (1, 1) string
    runLabel (1, 1) string
    options.SessionLabel (1, 1) string = ""
end

originalPath = path;
pathCleanup = onCleanup(@() path(originalPath));
addpath(char(eeglabRoot));
[~, ~, ~, ~] = eeglab('nogui');
textReadContract = verifyTextReadContract();

sourceRoot = resolveFolder(bidsRoot);

outputRoot = string(tempname);
mkdir(outputRoot);
outputCleanup = onCleanup(@() cleanupFolder(outputRoot));
outputRoot = resolveFolder(outputRoot);
assert(~startsWith(lower(outputRoot), lower(sourceRoot + filesep)), ...
    'Temporary derivative output overlaps the BIDS source.');

sourceBefore = snapshotTree(sourceRoot);
selectorArguments = { ...
    'subjects', {char(subjectLabel)}, ...
    'runs', {char(runLabel)}, ...
    'bidstask', char(taskLabel), ...
    'bidsevent', 'on', ...
    'bidschanloc', 'on' ...
};
if strlength(options.SessionLabel) > 0
    selectorArguments = [selectorArguments, ...
        {'sessions', {char(options.SessionLabel)}}];
end

lastwarn('');
[noWriteStudy, noWriteRecordings, noWriteBids, noWriteStats] = pop_importbids( ...
    char(sourceRoot), selectorArguments{:}, ...
    'metadata', 'on', 'outputdir', char(outputRoot));
[noWriteWarning, noWriteWarningId] = lastwarn;

lastwarn('');
[study, recordings, fullBids, fullStats] = pop_importbids( ...
    char(sourceRoot), selectorArguments{:}, ...
    'metadata', 'off', 'outputdir', char(outputRoot), ...
    'studyName', 'eeg-provenance-smoke');
[fullWarning, fullWarningId] = lastwarn;

assert(isscalar(recordings), ...
    'The selectors must resolve exactly one EEG recording.');
expectedBidsFields = [ ...
    "gInfo", "pInfo", "pInfoDesc", "eInfo", "eInfoDesc", ...
    "tInfo", "bidsstats", "scannedElectrodes", "behavioral" ...
];
assert(isfield(recordings(1), 'BIDS'), ...
    'The imported EEG representation has no EEG.BIDS field.');
actualBidsFields = string(fieldnames(recordings(1).BIDS));
assert(isempty(setxor(expectedBidsFields, actualBidsFields)), ...
    'EEG.BIDS fields differ from the pinned EEG-BIDS contract.');
expectedDatasetInfoFields = [ ...
    "filepath", "filename", "subject", "session", "run", ...
    "condition", "group", "index", "task" ...
];
actualDatasetInfoFields = string(fieldnames(study.datasetinfo));
assert(all(ismember(expectedDatasetInfoFields, actualDatasetInfoFields)), ...
    'STUDY.datasetinfo lacks a core identity field.');
sourceAfter = snapshotTree(sourceRoot);
sourceUnchanged = isequal(sourceBefore, sourceAfter);
assert(sourceUnchanged, 'EEG-BIDS changed the source file inventory.');

eventTypes = string({recordings(1).event.type});
[uniqueEventTypes, ~, eventGroups] = unique(eventTypes);
eventCounts = accumarray(eventGroups(:), 1);
outputEntries = dir(fullfile(outputRoot, "**", "*"));
outputEntries = outputEntries(~[outputEntries.isdir]);
outputFiles = string(fullfile({outputEntries.folder}, {outputEntries.name}));
outputFiles = erase(outputFiles, outputRoot + filesep);
outputExtensions = strings(numel(outputEntries), 1);
for outputIndex = 1:numel(outputEntries)
    [~, ~, outputExtension] = fileparts(outputEntries(outputIndex).name);
    outputExtensions(outputIndex) = lower(string(outputExtension));
end

result = struct;
result.matlab_version = string(version);
result.eeglab_version = string(eeg_getversion);
result.eegbids_version = string(bids_matlab_tools_ver);
result.text_read_contract = textReadContract;
result.selector = struct( ...
    "subject", subjectLabel, ...
    "session", options.SessionLabel, ...
    "task", taskLabel, ...
    "run", runLabel ...
);
result.no_write_pass = struct( ...
    "study_empty", isempty(noWriteStudy), ...
    "recording_count", numel(noWriteRecordings), ...
    "sample_payload_materialized", hasNumericPayload(noWriteRecordings), ...
    "bids_nonempty", ~isempty(noWriteBids), ...
    "stats_nonempty", ~isempty(noWriteStats), ...
    "warning", string(noWriteWarning), ...
    "warning_id", string(noWriteWarningId) ...
);
result.full_import = struct( ...
    "nbchan", recordings(1).nbchan, ...
    "srate", recordings(1).srate, ...
    "pnts", recordings(1).pnts, ...
    "trials", recordings(1).trials, ...
    "event_count", numel(recordings(1).event), ...
    "event_types", uniqueEventTypes, ...
    "event_counts", eventCounts, ...
    "chanloc_count", numel(recordings(1).chanlocs), ...
    "eeg_bids_fields", sort(actualBidsFields), ...
    "study_datasetinfo_fields", sort(actualDatasetInfoFields), ...
    "study_filename", string(study.filename), ...
    "bids_nonempty", ~isempty(fullBids), ...
    "stats_nonempty", ~isempty(fullStats), ...
    "warning", string(fullWarning), ...
    "warning_id", string(fullWarningId) ...
);
result.derivative_files = sort(outputFiles);
result.derivative_sidecar_copy_count = sum(ismember(outputExtensions, [".json", ".tsv"]));
result.source_file_count = height(sourceBefore);
result.source_unchanged = sourceUnchanged;
disp(jsonencode(result, PrettyPrint=true));

clear outputCleanup pathCleanup
end

function contract = verifyTextReadContract()
probeFile = string(tempname) + ".txt";
fileId = fopen(probeFile, 'w');
assert(fileId ~= -1, 'Could not create the text-read compatibility probe.');
fileCleanup = onCleanup(@() cleanupFile(probeFile));
fprintf(fileId, 'eeg-provenance');
fclose(fileId);

contract = struct;
contract.fileread_path = string(which('fileread'));
contract.string_path = false;
contract.character_vector_path = false;
contract.character_vector_error = "";
try
    fileread(probeFile);
    contract.string_path = true;
catch probeError
    error('eeg_provenance:TextReadStringPath', ...
        'MATLAB fileread failed its string-path smoke: %s', probeError.message);
end
try
    fileread(char(probeFile));
    contract.character_vector_path = true;
catch probeError
    contract.character_vector_error = string(probeError.message);
end
if ~contract.character_vector_path
    error('eeg_provenance:EEGBidsTextPathIncompatible', ...
        ['EEG-BIDS 10.5 passes character-vector JSON paths, but the active ' ...
         'fileread rejected them (%s). Use a compatible MATLAB/EEG-BIDS ' ...
         'release or upstream fix; do not shadow fileread.'], ...
        contract.character_vector_error);
end
clear fileCleanup
end

function cleanupFile(file)
if isfile(file)
    delete(file);
end
end

function materialized = hasNumericPayload(recordings)
materialized = false;
for recordingIndex = 1:numel(recordings)
    if isfield(recordings(recordingIndex), 'data') && ...
            isnumeric(recordings(recordingIndex).data)
        materialized = true;
        return
    end
end
end

function snapshot = snapshotTree(rootFolder)
entries = dir(fullfile(rootFolder, "**", "*"));
entries = entries(~[entries.isdir]);
paths = string(fullfile({entries.folder}, {entries.name}));
[paths, order] = sort(paths);
snapshot = table( ...
    paths(:), ...
    [entries(order).bytes].', ...
    [entries(order).datenum].', ...
    VariableNames=["Path", "Bytes", "ModifiedDateNumber"] ...
);
end

function cleanupFolder(folder)
if isfolder(folder)
    rmdir(folder, 's');
end
end

function resolvedFolder = resolveFolder(folder)
originalFolder = pwd;
folderCleanup = onCleanup(@() cd(originalFolder));
cd(folder);
resolvedFolder = string(pwd);
clear folderCleanup
end
