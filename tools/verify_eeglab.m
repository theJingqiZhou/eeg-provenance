function result = verify_eeglab(eeglabRoot, archiveSet)
%VERIFY_EEGLAB Exercise EEGLAB startup, plugin discovery, and SET I/O.

arguments
    eeglabRoot (1, 1) string
    archiveSet (1, 1) string = ""
end

originalPath = path;
pathCleanup = onCleanup(@() path(originalPath));
addpath(char(eeglabRoot));
[~, ~, ~, ~] = eeglab("nogui");

requiredFunctions = [ ...
    "pop_loadset", "pop_saveset", "eeg_checkset", ...
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

archive = struct("tested", false, "nbchan", [], "srate", [], "pnts", [], "trials", [], ...
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
    archiveEEG = eeg_checkset(archiveEEG);
    [warningMessage, warningId] = lastwarn;
    sourceAfter = dir(char(archiveSet));
    assert(sourceBefore.bytes == sourceAfter.bytes && sourceBefore.datenum == sourceAfter.datenum, ...
        "Archive SET file changed during metadata-only load");
    archive.tested = true;
    archive.nbchan = archiveEEG.nbchan;
    archive.srate = archiveEEG.srate;
    archive.pnts = archiveEEG.pnts;
    archive.trials = archiveEEG.trials;
    archive.warning_message = warningMessage;
    archive.warning_id = warningId;
end

result = struct;
result.matlab_version = version;
result.eeglab_version = eeg_getversion;
result.eegbids_version = bids_matlab_tools_ver;
result.eegbids_function = which("pop_importbids");
result.entry_points = entryPoints;
result.synthetic_shape = size(loaded.data);
result.synthetic_srate = loaded.srate;
result.archive = archive;
disp(jsonencode(result, PrettyPrint=true));
end

function cleanupFolder(folder)
if isfolder(folder)
    rmdir(folder, "s");
end
end
