import { Presets, SingleBar } from 'cli-progress';
import { createWriteStream, existsSync, mkdirSync, readFileSync, readdirSync, renameSync, rmSync, writeFileSync } from 'fs';
import { copy } from 'fs-extra';
import { pipeline } from 'stream/promises';
import { Extract } from 'unzip-stream';
import got from 'got';
import { setTimeout } from 'timers/promises';
import { compare, rcompare, valid } from 'semver';
import { marked } from 'marked';
import { htmlEscape } from 'escape-goat';

const modsToTrack = ["beat.click-sound"] // click sounds server
const modsToTrack2 = ["uproxide.user_reviews"] // user reviews server
const modsToTrack3 = ["uproxide.user_reviews", "uproxide.geodedevelopers", "uproxide.accupracatt", "uproxide.autosong", "uproxide.more_difficulties", "uproxide.evilgd", "uproxide.quotes", "riley.nogrounds", "thesillydoggo.icon_kit_switcher"] // uproxides little land
const modsToTrack4 = ["cdc.level_thumbnailss"] // Level Thumbnails server

/*if (!existsSync('src')) {
    console.error('This script must be run in the repo root!');
    process.exit(1);
}*/

const indexBar = new SingleBar({
    format: '{bar} {percentage}% {status}'
}, Presets.shades_classic);

indexBar.start(100, 0, { status: 'Downloading mods index' });

// Download mods index
if (!existsSync('_mods_tmp') || process.argv.at(2) === '-r') {
    rmSync('_mods_tmp', { recursive: true, force: true });

    await pipeline(
        got.stream('https://github.com/geode-sdk/mods/archive/refs/heads/main.zip')
            .on('downloadProgress', prog => {
                indexBar.update(prog.percent * 99);
            }),
        Extract({ path: '__mods' })
    );
    
    indexBar.update(99, { status: 'Moving files' })
    renameSync('__mods/mods-main/mods-v2', '_mods_tmp');
    rmSync('__mods', { recursive: true, force: true });

    indexBar.update(100, { status: 'Mods index downloaded' });
} else {
    indexBar.update(100, { status: 'Using cached mods index' });
}
indexBar.stop();
indexBar.start(100, 0, { status: 'Downloading Coop\'s mod index' });

if (!existsSync('_mods2_tmp') || process.argv.at(2) === '-r') {
    rmSync('_mods2_tmp', { recursive: true, force: true });

    await pipeline(
        got.stream('https://github.com/coopeeo/geodemodindex/archive/refs/heads/mods.zip')
            .on('downloadProgress', prog => {
                indexBar.update(prog.percent * 99);
            }),
        Extract({ path: '__mods2' })
    );
    
    indexBar.update(99, { status: 'Moving files' })
    renameSync('__mods2/geodemodindex-mods/mods-v2', '_mods2_tmp');
    rmSync('__mods2', { recursive: true, force: true });

    indexBar.update(100, { status: 'Mods index downloaded' });
}
else {
    indexBar.update(100, { status: 'Using cached mods index' });
}


const modsBar = new SingleBar({
    format: '{bar} {percentage}% {status}'
}, Presets.shades_classic);
modsBar.start(100, 0, { status: 'Parsing mods' });

function tryReadFile(path, or = undefined) {
    try {
        return readFileSync(path);
    }
    catch {
        return or ? tryReadFile(or) : undefined;
    }
}

// Iterate downloaded mods to construct the browse page first
const mods = readdirSync('_mods_tmp', { withFileTypes: true })
    .filter(dir => dir.isDirectory())
    .map((dir, i, arr) => {
        const d = `${dir.path}/${dir.name}`;
        modsBar.update(i / arr.length * 100);
        return {
            id: dir.name,
            versions: readdirSync(d, { withFileTypes: true })
                .filter(dir => dir.isDirectory() && valid(dir.name))
                .map(ver => {
                    return {
                        version: ver.name,
                        modJSON: JSON.parse(readFileSync(`${ver.path}/${ver.name}/mod.json`).toString()),
                        entryJSON: JSON.parse(readFileSync(`${ver.path}/${ver.name}/entry.json`).toString()),
                    };
                })
                .sort((a, b) => rcompare(a.version, b.version)),
            about: tryReadFile(`${d}/about.md`)?.toString() ?? "No description provided",
            changelog: tryReadFile(`${d}/changelog.md`)?.toString() ?? "No changelog provided",
            // logo: tryReadFile(`${d}/logo.png`, 'media/no-logo.png'),
            logoURL: existsSync(`${d}/logo.png`) ?
                `https://raw.githubusercontent.com/geode-sdk/mods/main/mods-v2/${dir.name}/logo.png` :
                `https://raw.githubusercontent.com/geode-sdk/geode/main/loader/resources/logos/no-logo.png`
        };
    })
    .filter(x => {
        let latestVer = x.versions[0];
        let geodeVer = latestVer.modJSON.geode;
        // Only show mods that target geode v2
        return (geodeVer.startsWith('2.') || geodeVer.startsWith('v2.')) && !!latestVer.modJSON.gd;
    });

modsBar.update(100, { status: 'Mods parsed' });
modsBar.stop();
modsBar.start(100, 0, { status: 'Parsing mods from Coop\'s repo' });

const modscompare = readdirSync('_mods2_tmp', { withFileTypes: true })
    .filter(dir => dir.isDirectory())
    .map((dir, i, arr) => {
        const d = `${dir.path}/${dir.name}`;
        modsBar.update(i / arr.length * 100);
        return {
            id: dir.name,
            versions: readdirSync(d, { withFileTypes: true })
                .filter(dir => dir.isDirectory() && valid(dir.name))
                .map(ver => {
                    return {
                        version: ver.name,
                        modJSON: JSON.parse(readFileSync(`${ver.path}/${ver.name}/mod.json`).toString()),
                        entryJSON: JSON.parse(readFileSync(`${ver.path}/${ver.name}/entry.json`).toString()),
                    };
                })
                .sort((a, b) => rcompare(a.version, b.version)),
            about: tryReadFile(`${d}/about.md`)?.toString() ?? "No description provided",
            changelog: tryReadFile(`${d}/changelog.md`)?.toString() ?? "No changelog provided",
            // logo: tryReadFile(`${d}/logo.png`, 'media/no-logo.png'),
            logoURL: existsSync(`${d}/logo.png`) ?
                `https://raw.githubusercontent.com/geode-sdk/mods/main/mods-v2/${dir.name}/logo.png` :
                `https://raw.githubusercontent.com/geode-sdk/geode/main/loader/resources/logos/no-logo.png`
        };
    })
    .filter(x => {
        let latestVer = x.versions[0];
        let geodeVer = latestVer.modJSON.geode;
        // Only show mods that target geode v2
        return (geodeVer.startsWith('2.') || geodeVer.startsWith('v2.')) && !!latestVer.modJSON.gd;
    });
modsBar.update(100, { status: 'Mods parsed' });
modsBar.stop()
modsBar.start(100, 0, { status: 'Parsing mods from Coop\'s repo into object instead of array' });
var modscomparereel = {}
for (let index = 0; index < modscompare.length; index++) {
    const element = modscompare[index];
    modscomparereel[element.id] = element
    //console.log("The og element (" + element.id + "): ",element)
    //console.log("The new element (" + element.id + "): ",element)
    //console.log(modscomparereel,modscompare[index])
    modsBar.update(index / modscompare.length * 100);
}
modsBar.update(100, { status: 'Mods parsed' });
modsBar.stop();

const genBar = new SingleBar({
    format: '{bar} {percentage}% {status}'
}, Presets.shades_classic);
genBar.start(100, 0, { status: 'Copying files' });

//rmSync('gen/mods/[mod.id]', { recursive: true, force: true });

genBar.update(0, { status: 'Constructing pages' });

//const modPageTemplate = readFileSync('src/mods/[mod.id]/index.html').toString();
const searchPageContent = [];

function withIfEmpty(arr, elem) {
    if (!arr.length) {
        arr.push(elem);
    }
    return arr;
}

function cutText(text) {
    if (text.length > 70) {
        return text.substring(0, 67) + "...";
    }
    else {
        return text;
    }
}

function escape(x) {
    return htmlEscape(String(x));
}

function html(parts) {
    let result = parts[0];
    for (let i = 1; i < parts.length; ++i) {
        result += escape(arguments[i]) + parts[i];
    }
    return result;
}

function pathEscape(x) {
    return x.replaceAll(/\.{2,}/g, '.') // Remove multiple dots
}

function filepath(parts) {
    let result = parts[0];
    for (let i = 1; i < parts.length; ++i) {
        result += pathEscape(arguments[i]) + parts[i];
    }
    return result;
}

function developersTextOnListing(developers) {
    if (developers.length == 0) return "No Developer Found";
    if (developers.length <= 2) return developers.join(" & ");
    return developers[0] + " + " + (developers.length - 1) + " more "
}
var shouldWeUpdateIndex = false
var lenumberofmod=-1
var theLeObject = []
var theLeObjectx = []
var theLeObjectxxx = []
var theLeObjectxxxx = []
var theLeObjectxxxxx = []
for (const mod of mods) {
    if (modscomparereel[mod.id]){
    //console.log("The new element in mod for state (" + modscomparereel[mod.id].id + "): ",modscomparereel[mod.id])
    //console.log("------------------------------------------------------------------------------- " + mod.id + " -------------------------------------------------------------------------------")
    //console.log("The new versions element in mod for state (" + mod.id + "): ",modscomparereel[mod.id].versions)
    lenumberofmod+=1
    var modVersion = mod.versions[0].version
    // Compare mod to see if it updated with coop's repo
    if (modVersion != modscomparereel[mod.id].versions[0].version){// && modsToTrack.includes(mod.id)){
        shouldWeUpdateIndex=true;
        var daver = mod.versions[0]
        daver.changelog = mod.changelog
        daver.about = mod.about
        daver.bundleId= mod.id
        daver.tags = "arrow_up"
        daver.tags2 = "Update"
        daver.tags3 = "update"
        theLeObject.push(daver)
        if (modsToTrack.includes(mod.id)){theLeObjectx.push(daver);}
        if (modsToTrack2.includes(mod.id)){theLeObjectxxx.push(daver);}
        if (modsToTrack3.includes(mod.id)){theLeObjectxxxx.push(daver);}
    }
    

    
    genBar.update(searchPageContent.length / mods.length * 99);
}else{//if(modsToTrack.includes(mod.id)){
    shouldWeUpdateIndex=true;
    var daver = mod.versions[0]
    daver.changelog = mod.changelog
    daver.about = mod.about
    daver.bundleId= mod.id
    daver.tags = "heavy_plus_sign"
    daver.tags2 = "New Mod"
    daver.tags3 = "new"
    theLeObject.push(daver)
    if (modsToTrack.includes(mod.id)){theLeObjectx.push(daver);}
    if (modsToTrack2.includes(mod.id)){theLeObjectxxx.push(daver);}
    if (modsToTrack3.includes(mod.id)){theLeObjectxxxx.push(daver);}
}}//}

console.log(`::set-output name=update_index::${shouldWeUpdateIndex}`);
console.log(`::set-output name=list_index::${JSON.stringify(theLeObject)}`);
console.log(`::set-output name=list_indexx::${JSON.stringify(theLeObjectx)}`);
console.log(`::set-output name=list_indexxx::${JSON.stringify(theLeObjectxxx)}`);
console.log(`::set-output name=list_indexxxx::${JSON.stringify(theLeObjectxxxx)}`);
console.log(`::set-output name=list_indexxxxx::${JSON.stringify(theLeObjectxxxxx)}`);
genBar.update(99, { status: 'Writing search page' });
genBar.update(100, { status: 'Pages finished' });
genBar.stop();