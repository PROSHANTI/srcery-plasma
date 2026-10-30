import QtQuick
import QtQuick.Window
Window {
    id: window
    visible: true
    width: 3840; height: 2160
    color: "#1C1B19"
    Image {
        id: scene
        anchors.fill: parent
        source: "share/wallpapers/Srcery/contents/images/3840x2160.svg"
        sourceSize.width: window.width
        sourceSize.height: window.height
        fillMode: Image.PreserveAspectFit
        Image {
            x: 1620; y: 760; width: 600; height: 520
            source: "share/plasma/look-and-feel/org.srcery.desktop/contents/splash/images/logo.svg"
            sourceSize.width: 1200; sourceSize.height: 1040
            fillMode: Image.PreserveAspectFit
        }
    }
    Timer {
        interval: 1200; running: true
        onTriggered: scene.grabToImage(function(result) {
            const path = Qt.resolvedUrl("share/wallpapers/Srcery/contents/images/3840x2160.png").toString().replace("file://", "")
            const ok = result.saveToFile(path)
            console.log("WALLPAPER_RENDER", ok)
            Qt.exit(ok ? 0 : 1)
        })
    }
}
