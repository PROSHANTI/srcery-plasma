import QtQuick
import QtQuick.Window
Window {
 id: win; visible: true; width: 1600; height: 900; color: "#1C1B19"
 Rectangle {
  id: scene; anchors.fill: parent; color: "#1C1B19"
  Image { anchors.fill: parent; source: "share/wallpapers/Srcery/contents/images/3840x2160.png"; fillMode: Image.PreserveAspectCrop }
  Rectangle {
   x: 70; y: 145; width: 470; height: 610; radius: 14; color: "#262626"; border.color: "#444444"
   Column {
    anchors.fill: parent; anchors.margins: 36; spacing: 22
    Text { text: "SRCERY"; color: "#FCE8C3"; font.family: "Iosevka"; font.pixelSize: 48 }
    Text { text: "KDE Plasma 6"; color: "#BAA67F"; font.family: "Iosevka"; font.pixelSize: 24 }
    Rectangle { width: 398; height: 1; color: "#444444" }
    Text { text: "Warm charcoal\nParchment text\nGold accents"; color: "#FCE8C3"; font.family: "Iosevka"; font.pixelSize: 27; lineHeight: 1.45 }
    Row { spacing: 13; Repeater { model: ["#EF2F27","#519F50","#FBB829","#2C78BF","#E02C6D","#0AAEB3"]
     Rectangle { required property string modelData; width: 44; height: 44; radius: 22; color: modelData }
    } }
    Text { text: "Iosevka\nAa Бб Вв 0123456789"; color: "#BAA67F"; font.family: "Iosevka"; font.pixelSize: 27; lineHeight: 1.4 }
    Rectangle { width: 398; height: 53; radius: 6; color: "#FBB829"
     Text { anchors.centerIn: parent; text: "SRCERY Plasma"; color: "#1C1B19"; font.family: "Iosevka"; font.pixelSize: 24 }
    }
   }
  }
  Text { anchors.right: parent.right; anchors.bottom: parent.bottom; anchors.margins: 26; text: "Unofficial community adaptation · palette and wallpaper preview"; color: "#918175"; font.family: "Iosevka"; font.pixelSize: 16 }
 }
 Timer { interval: 1400; running: true; onTriggered: scene.grabToImage(function(r) { const ok=r.saveToFile(Qt.resolvedUrl("Public-preview.png").toString().replace("file://", "")); r.saveToFile(Qt.resolvedUrl("Public-preview.jpg").toString().replace("file://", "")); console.log("PREVIEW_SAVED",ok); Qt.exit(ok?0:1); }) }
}
