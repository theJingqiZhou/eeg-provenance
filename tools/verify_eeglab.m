function result = verify_eeglab(eeglabRoot, archiveSet)
%VERIFY_EEGLAB Exercise EEGLAB startup, SET metadata, and STUDY construction.

arguments
    eeglabRoot (1, 1) string
    archiveSet (1, 1) string = ""
end

originalPath = path;
pathCleanup = onCleanup(@() path(originalPath));
addpath(char(eeglabRoot));
[~, ~, ~, ~] = eeglab("nogui");

requiredFunctions = [ ...
    "pop_loadset", "pop_saveset", "eeg_checkset", "std_editset", ...
    "pop_importbids", "pop_exportbids", ...
    "pop_eegfiltnew", "pop_reref", "pop_interp", ...
    "pop_runica", "pop_iclabel", "pop_clean_rawdata", ...
    "pop_dipfit_settings" ...
];
entryPoints = struct;
for functionName = requiredFunctions
    functionPath = string(which(functionName));
    assert(strlength(functionPath) > 0, ...
        "Missing required EEGLAB function: %s", functionName);
    entryPoints.(functionName) = functionPath;
end

optionalFunctions = [ ...
    "pop_loadbv", "pop_biosig", "sopen", "pop_fileio", ...
    "pop_ctf_read", "pop_MEF3", "GEDAI", "pop_GEDAI" ...
];
optionalEntryPoints = struct;
for functionName = optionalFunctions
    optionalEntryPoints.(functionName) = string(which(functionName));
end

EEG = eeg_emptyset;
EEG.setname = "eeg-provenance-synthetic";
EEG.nbchan = 4;
EEG.srate = 256;
EEG.pnts = 512;
EEG.trials = 1;
EEG.xmin = 0;
EEG.xmax = (EEG.pnts - 1) / EEG.srate;
EEG.times = (0:(EEG.pnts - 1)) / EEG.srate * 1000;
rng(97, "twister");
EEG.data = randn(EEG.nbchan, EEG.pnts) * 5;
labels = {"Fz", "Cz", "Pz", "Oz"};
for index = 1:numel(labels)
    EEG.chanlocs(index).labels = labels{index};
end
EEG = eeg_checkset(EEG);

roundTripFolder = tempname;
mkdir(roundTripFolder);
folderCleanup = onCleanup(@() cleanupFolder(roundTripFolder));
pop_saveset(EEG, 'filename', 'synthetic.set', 'filepath', roundTripFolder, 'savemode', 'onefile');
loaded = pop_loadset('filename', 'synthetic.set', 'filepath', roundTripFolder, 'loadmode', 'all');
loaded = eeg_checkset(loaded);
assert(isequal(size(loaded.data), [4, 512]), "Synthetic SET round trip changed data shape");
assert(loaded.srate == 256, "Synthetic SET round trip changed sampling rate");

oneFileInfo = pop_loadset( ...
    'filename', 'synthetic.set', 'filepath', roundTripFolder, 'loadmode', 'info');
assert(~isnumeric(oneFileInfo.data), ...
    "One-file SET metadata load unexpectedly materialized samples");

secondEEG = EEG;
secondEEG.setname = "eeg-provenance-synthetic-two-file";
pop_saveset(secondEEG, 'filename', 'synthetic-two.set', ...
    'filepath', roundTripFolder, 'savemode', 'twofiles');
twoFileInfo = loadSetInfoFromFolder('synthetic-two.set', roundTripFolder);
assert(~isnumeric(twoFileInfo.data), ...
    "Two-file SET metadata load materialized samples from its own folder");

studyPath = fullfile(roundTripFolder, 'synthetic.study');
studyCommands = { ...
    {'index', 1, 'load', fullfile(roundTripFolder, 'synthetic.set'), ...
     'subject', 'sub-01', 'session', 1, 'run', 1, 'task', 'smoke'}, ...
    {'index', 2, 'load', fullfile(roundTripFolder, 'synthetic-two.set'), ...
     'subject', 'sub-02', 'session', 1, 'run', 1, 'task', 'smoke'} ...
};
[study, studySets] = std_editset([], [], 'commands', studyCommands, ...
    'filename', studyPath, 'task', 'smoke');
assert(numel(study.datasetinfo) == 2 && numel(studySets) == 2, ...
    "Synthetic STUDY did not retain both SET datasets");
assert(strcmp(study.datasetinfo(1).subject, 'sub-01') && ...
    strcmp(study.datasetinfo(2).subject, 'sub-02'), ...
    "Synthetic STUDY changed subject identities");

archive = struct("tested", false, "nbchan", [], "srate", [], "pnts", [], "trials", [], ...
    "data_materialized", [], "data_descriptor", "", ...
    "warning_message", "", "warning_id", "");
if strlength(archiveSet) > 0
    assert(isfile(archiveSet), "Archive SET file does not exist: %s", archiveSet);
    sourceBefore = dir(char(archiveSet));
    [archiveFolder, archiveName, archiveExtension] = fileparts(char(archiveSet));
    lastwarn('');
    archiveEEG = pop_loadset( ...
        'filename', [archiveName archiveExtension], ...
        'filepath', archiveFolder, ...
        'loadmode', 'info');
    [warningMessage, warningId] = lastwarn;
    sourceAfter = dir(char(archiveSet));
    assert(sourceBefore.bytes == sourceAfter.bytes && sourceBefore.datenum == sourceAfter.datenum, ...
        "Archive SET file changed during metadata-only load");
    archive.tested = true;
    archive.nbchan = archiveEEG.nbchan;
    archive.srate = archiveEEG.srate;
    archive.pnts = archiveEEG.pnts;
    archive.trials = archiveEEG.trials;
    archive.data_materialized = isnumeric(archiveEEG.data);
    if ischar(archiveEEG.data) || isstring(archiveEEG.data)
        archive.data_descriptor = string(archiveEEG.data);
    end
    archive.warning_message = warningMessage;
    archive.warning_id = warningId;
end

result = struct;
result.matlab_version = version;
result.eeglab_version = eeg_getversion;
result.eegbids_version = bids_matlab_tools_ver;
result.eegbids_function = which("pop_importbids");
result.entry_points = entryPoints;
result.optional_entry_points = optionalEntryPoints;
result.synthetic_shape = size(loaded.data);
result.synthetic_srate = loaded.srate;
result.one_file_info_data = string(oneFileInfo.data);
result.two_file_info_data = string(twoFileInfo.data);
result.study_datasetinfo_fields = fieldnames(study.datasetinfo);
result.study_subjects = string({study.datasetinfo.subject});
result.archive = archive;
disp(jsonencode(result, PrettyPrint=true));
end

function infoEEG = loadSetInfoFromFolder(filename, folder)
originalFolder = pwd;
folderCleanup = onCleanup(@() cd(originalFolder));
cd(folder);
infoEEG = pop_loadset('filename', filename, 'filepath', folder, 'loadmode', 'info');
end

function cleanupFolder(folder)
if isfolder(folder)
    rmdir(folder, "s");
end
end
