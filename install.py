#!/usr/bin/env python3
"""Install SRCERY Plasma entirely in the current user's home. No network or sudo."""
import argparse, datetime, json, os, pathlib, shutil, subprocess, sys
P=pathlib.Path
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--apply',action='store_true',help='Apply theme, fonts and grey logo wallpaper now')
parser.add_argument('--keep-wallpaper',action='store_true',help='Keep current desktop wallpaper when applying')
parser.add_argument('--tela-source',type=P,help='Optional official Tela Circle source directory, already downloaded and reviewed')
args=parser.parse_args()
if os.geteuid()==0:sys.exit('Run as your desktop user, without sudo.')
root=P(__file__).resolve().parent
home=P.home(); data=P(os.environ.get('XDG_DATA_HOME',home/'.local/share')); config=P(os.environ.get('XDG_CONFIG_HOME',home/'.config'))
state=P(os.environ.get('XDG_STATE_HOME',home/'.local/state'))/'srcery-plasma'
for command in ('fc-cache','kpackagetool6'):
 if not shutil.which(command):sys.exit('Missing dependency: '+command)
if args.apply:
 for command in ('plasma-apply-lookandfeel','plasma-apply-colorscheme','kwriteconfig6','qdbus6'):
  if not shutil.which(command):sys.exit('Missing dependency: '+command)
 if not os.environ.get('DBUS_SESSION_BUS_ADDRESS'):sys.exit('Run --apply inside your Plasma desktop session.')
tela=args.tela_source.resolve() if args.tela_source else None
if tela and not (tela/'install.sh').is_file():sys.exit('Tela source must contain install.sh')
base='Srcery-Circle-FBB829'; icon=base+'-dark'
if tela and any((data/'icons'/(base+s)).exists() for s in ('','-light','-dark')):
 sys.exit('SRCERY Circle already exists. Omit --tela-source to reuse it; no icon files were overwritten.')
stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'); backup=state/'backups'/stamp;backup.mkdir(parents=True)
targets=['plasma/look-and-feel/org.srcery.desktop','plasma/desktoptheme/Srcery','color-schemes/Srcery.colors','wallpapers/Srcery','konsole/Srcery.colorscheme','konsole/Srcery.profile','fonts/Srcery']
manifest=[]
def backup_file(src,dst):
 if src.is_symlink():sys.exit('Refusing to overwrite symlink: '+str(src))
 if src.is_dir():shutil.copytree(src,dst,symlinks=True)
 elif src.exists():dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
for rel in targets:
 source=root/'share'/rel;target=data/rel
 manifest.append({'target':str(target),'existed':target.exists()})
 backup_file(target,backup/'data'/rel)
 if source.is_dir():shutil.copytree(source,target,dirs_exist_ok=True)
 else:target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
for rel in ['kdeglobals','kwinrc','plasmarc','ksplashrc','kcminputrc','konsolerc','kdedefaults','plasma-org.kde.plasma.desktop-appletsrc','gtk-3.0/settings.ini','gtk-4.0/settings.ini']:
 backup_file(config/rel,backup/'config'/rel)
(backup/'manifest.json').write_text(json.dumps(manifest,indent=2))
shutil.copytree(root/'LICENSES',data/'srcery-plasma/LICENSES',dirs_exist_ok=True)
shutil.copy2(root/'NOTICE',data/'srcery-plasma/NOTICE')
def run(argv):subprocess.run([str(a) for a in argv],check=True)
if tela:
 run(['bash',tela/'install.sh','-d',data/'icons','-n','Srcery-Circle','-c','FBB829'])
if not (data/'icons'/icon/'index.theme').exists():icon='breeze-dark'
defaults=data/'plasma/look-and-feel/org.srcery.desktop/contents/defaults'
defaults.write_text(defaults.read_text().replace('Theme=breeze-dark','Theme='+icon))
run(['fc-cache','-f',data/'fonts/Srcery'])
run(['kpackagetool6','--type','Plasma/LookAndFeel','--show','org.srcery.desktop'])
if args.apply:
 run(['plasma-apply-lookandfeel','--apply','org.srcery.desktop'])
 # The accent-color mode ignores positional scheme arguments; persist the scheme first.
 run(['kwriteconfig6','--file','kdeglobals','--group','General','--key','ColorScheme','Srcery'])
 run(['plasma-apply-colorscheme','--accent-color','transparent'])
 def write(file,group,key,value):run(['kwriteconfig6','--file',file,'--group',group,'--key',key,value])
 write('kdeglobals','KDE','widgetStyle','Breeze');write('kdeglobals','Icons','Theme',icon)
 for key,size in [('font',12),('fixed',12),('smallestReadableFont',10),('menuFont',12),('toolBarFont',12)]:
  write('kdeglobals','General',key,f'Iosevka,{size},-1,5,50,0,0,0,0,0')
 write('kdeglobals','WM','activeFont','Iosevka,12,-1,5,50,0,0,0,0,0')
 write('kwinrc','org.kde.kdecoration2','library','org.kde.breeze')
 # Breeze GTK supplied by KDE follows the active palette; no host-specific GTK CSS is shipped.
 for version in ('3.0','4.0'):
  write('gtk-'+version+'/settings.ini','Settings','gtk-theme-name','Breeze')
  write('gtk-'+version+'/settings.ini','Settings','gtk-application-prefer-dark-theme','true')
  write('gtk-'+version+'/settings.ini','Settings','gtk-font-name','Iosevka 12')
  write('gtk-'+version+'/settings.ini','Settings','gtk-icon-theme-name',icon)
 if not args.keep_wallpaper:
  image=(data/'wallpapers/Srcery/contents/images/3840x2160.png').as_uri()
  js='for (const d of desktops()) { d.wallpaperPlugin="org.kde.image"; d.currentConfigGroup=["Wallpaper","org.kde.image","General"]; d.writeConfig("Image",'+json.dumps(image)+'); } print("SRCERY wallpaper applied");'
  run(['qdbus6','org.kde.plasmashell','/PlasmaShell','org.kde.PlasmaShell.evaluateScript',js])
 print('Applied SRCERY. Existing panels and widgets were preserved. Restart individual apps if needed.')
print('Installed SRCERY Plasma 1.0.0. Icons: '+icon)
print('Backup: '+str(backup))
print('To apply later: python3 install.py --apply')
