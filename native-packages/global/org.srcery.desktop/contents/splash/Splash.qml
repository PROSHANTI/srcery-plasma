import QtQuick 2.15

Rectangle {
    id: root
    property int stage: 0
    color: "#1C1B19"
    Image {
        id: logo
        anchors.centerIn: parent
        anchors.verticalCenterOffset: -30
        width: Math.min(parent.width * 0.28, 280)
        height: width * 520 / 600
        source: "images/logo.svg"
        sourceSize.width: width * 2
        sourceSize.height: height * 2
        fillMode: Image.PreserveAspectFit
        opacity: 0
        NumberAnimation on opacity { from: 0; to: 1; duration: 650; easing.type: Easing.OutCubic }
    }
    Rectangle {
        width: 128; height: 2; radius: 1
        color: "#444444"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: Math.max(52, parent.height * 0.12)
        Rectangle {
            height: parent.height; radius: 1
            width: parent.width * Math.max(0.06, Math.min(1, root.stage / 6))
            color: "#FBB829"
            Behavior on width { NumberAnimation { duration: 350; easing.type: Easing.OutCubic } }
        }
    }
}
