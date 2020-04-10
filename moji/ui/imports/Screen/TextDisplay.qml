import QtQuick 1.1
import eroge.moji 1.0

Item {
    id: root

    function changeText(text) {
        textedit.text = text
    }
//    Component.onCompleted: showText()

    width: 200
    height: 200

    Rectangle {
        id: headerBar

        anchors {
            left: root.left
            leftMargin: 10//-9
            bottom: root.bottom//root.top
            bottomMargin: 4
        }
        radius: 9
        height: 20
        width: buttonRow.width * 2
        visible: true
        color: '#33000000'
        opacity: 1

        Row {
            id: buttonRow

            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                leftMargin: 1
            }
            spacing: 2
            width: 40
        }
        MouseArea {
            id: dragArea

            anchors.fill: parent
            acceptedButtons: Qt.LeftButton
            drag {
                target: root
                axis: Drag.XandYAxis
            }
        }
    }
    TextEdit {
        id: textedit

        text: "にほんごのテストはこちらへ"
        width: root.width
        color: 'snow'
        font {
            pixelSize: 34
            family: 'MS Gothic'
            bold: true
        }
        effect: Glow {
            offset: '1,1'
            blurRadius: 8
            blurIntensity: 2
            enabled: true
            color: 'red'
        }
        anchors.centerIn: parent
        textFormat: TextEdit.RichText
        readOnly: false
        focus: false
        wrapMode: TextEdit.Wrap
        verticalAlignment: TextEdit.AlignVCenter
        horizontalAlignment: TextEdit.AlignLeft

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.LeftButton
            enabled: !!textedit.text
            hoverEnabled: enabled
        }
    }
//    Python plugin
//    ReciveText {
//        id: textPlugin

//        Component.onCompleted: {
//            textPlugin.showText.connect(root.changeText)
//        }
//    }
}
