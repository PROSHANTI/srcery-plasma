import configparser, hashlib, json, os, pathlib, re, subprocess, tarfile, tempfile

results=[]
for baseline in ('fresh','fresh-custom-xdg','1.0.0','1.1.0','interrupted-1.0.0'):
    with tempfile.TemporaryDirectory(prefix='srcery-single-package-') as home:
        h=pathlib.Path(home)
        data=h/('.local/share' if baseline=='fresh' else 'custom-data')
        config=h/'config'
        env=os.environ.copy()
        env.update(HOME=home,XDG_DATA_HOME=str(data),XDG_CONFIG_HOME=str(config),
                   XDG_CACHE_HOME=home+'/cache',XDG_STATE_HOME=home+'/state',
                   XDG_CONFIG_DIRS=str(config/'kdedefaults')+':/etc/xdg',
                   XDG_DATA_DIRS='/usr/local/share:/usr/share',QT_QPA_PLATFORM='offscreen',
                   QT_QPA_PLATFORMTHEME='kde',QT_QUICK_BACKEND='software',QT_FORCE_STDERR_LOGGING='1',QT_LOGGING_TO_CONSOLE='1',LANG='C.UTF-8')
        env.pop('QT_STYLE_OVERRIDE',None)
        env.pop('QT_DATA_HOME',None)
        def run(args,timeout=60):
            p=subprocess.run(['dbus-run-session','--',*args],env=env,capture_output=True,text=True,timeout=timeout)
            if p.returncode:raise RuntimeError((baseline,args[0],p.returncode,re.sub(r'https?://[^\s\"<>]+','[URL omitted]',p.stdout+p.stderr)[-3500:]))
            return p.stdout,p.stderr
        if baseline in ('1.0.0','interrupted-1.0.0'):
            source=h/'original';source.mkdir()
            with tarfile.open('/tmp/SRCERY-Plasma-1.0.0.tar.gz') as t:t.extractall(source,filter='data')
            run(['python3',str(source/'SRCERY-Plasma-1.0.0/install.py')])
            if baseline=='interrupted-1.0.0':
                import shutil
                shutil.rmtree(data/'plasma/look-and-feel/org.srcery.desktop')
        elif baseline=='1.1.0':
            for file,target in [('SRCERY-Global-1.1.0.tar.gz','plasma/look-and-feel'),('SRCERY-Plasma-Style-1.1.0.tar.gz','plasma/desktoptheme'),('SRCERY-Wallpaper-1.1.0.tar.gz','wallpapers')]:
                dest=data/target;dest.mkdir(parents=True,exist_ok=True)
                with tarfile.open('/tmp/'+file) as t:t.extractall(dest,filter='data')
        legacy=data/'plasma/desktoptheme/Srcery/metadata.json'
        before_legacy=legacy.read_bytes() if legacy.exists() else None
        if baseline in ('1.0.0','interrupted-1.0.0'):assert 'KPackageStructure' not in json.loads(before_legacy)
        config.mkdir(parents=True,exist_ok=True)
        desktop=config/'plasma-org.kde.plasma.desktop-appletsrc'
        desktop.write_text('[Containments][190]\nwallpaperplugin=org.kde.slideshow\n[Containments][190][Wallpaper][org.kde.slideshow][General]\nSlidePaths=/tmp/pictures/\nSlideInterval=300\n[Containments][191]\nplugin=org.kde.panel\nlocation=3\n')
        globals_file=config/'kdeglobals';globals_file.write_text('[Icons]\nTheme=TestRoundIcons\n')
        before_desktop=desktop.read_bytes()
        existing=(data/'plasma/look-and-feel/org.srcery.desktop').exists()
        run(['kpackagetool6','--type','Plasma/LookAndFeel','--upgrade' if existing else '--install','/tmp/SRCERY-Plasma-1.2.0.tar.gz'])
        package=data/'plasma/look-and-feel/org.srcery.desktop'
        meta=json.loads((package/'metadata.json').read_text())
        assert meta['KPlugin']['Version']=='1.2.0'
        assert not meta.get('X-KPackage-Dependencies')
        if before_legacy is not None:assert legacy.read_bytes()==before_legacy
        run(['plasma-apply-lookandfeel','--apply','org.srcery.desktop'])
        c=configparser.ConfigParser(interpolation=None);c.optionxform=str
        c.read([config/'kdedefaults/kdeglobals',config/'kdeglobals'])
        assert c['Colors:Window']['BackgroundNormal']=='28,27,25'
        assert c['Colors:Window']['ForegroundNormal']=='252,232,195'
        assert c['Colors:Selection']['BackgroundNormal']=='251,184,41'
        assert c['Icons']['Theme']=='TestRoundIcons'
        assert c['General']['font'].startswith('Iosevka,')
        p=configparser.ConfigParser(interpolation=None);p.read([config/'kdedefaults/plasmarc',config/'plasmarc'])
        assert p['Theme']['name']=='default'
        wallpaper=run(['kreadconfig6','--file',str(package/'contents/defaults'),'--group','Wallpaper','--key','Image'])[0].strip()
        assert wallpaper==str(package/'contents/wallpaper'),wallpaper
        assert (pathlib.Path(wallpaper)/'contents/images/3840x2160.png').is_file()
        assert desktop.read_bytes()==before_desktop
        qml=h/'colors.qml'
        qml.write_text('import QtQuick\nimport org.kde.kirigami as K\nimport org.kde.plasma.components as PC\nPC.Label { id: root; text: "SRCERY"; property color testBackground: K.Theme.backgroundColor; property color testText: K.Theme.textColor; Timer { interval: 200; running: true; onTriggered: { console.log("SRCERY_PLASMA_COLORS", root.testBackground.toString(), root.testText.toString()); Qt.quit(); } } }\n')
        out,err=run(['timeout','15','qml6',str(qml)],20)
        match=re.search(r'SRCERY_PLASMA_COLORS (#\w+) (#\w+)',out+err)
        assert match and match.groups()==('#1c1b19','#fce8c3'),(out,err)
        result={'baseline':baseline,'version':'1.2.0','external_dependencies':0,'legacy_style_unchanged':True,
                'palette_applied':True,'breeze_plasma_colors':list(match.groups()),'embedded_wallpaper_resolved':True,
                'round_icon_choice_preserved':True,'slideshow_and_panels_preserved':True}
        results.append(result);print(json.dumps(result),flush=True)
print('ALL_SINGLE_PACKAGE_CASES_PASSED',flush=True)
