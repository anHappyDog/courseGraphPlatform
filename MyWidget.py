import math
import random
import time
import typing

from PyQt5.QtCore import QPointF, Qt, QEvent
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QStyleOptionGraphicsItem, QWidget, QGraphicsTextItem, \
    QGraphicsEllipseItem, QGraphicsLineItem
from neo4j import GraphDatabase

from AppInfo import AppInfo
from MySignals import myNodeResultSignal, myChangeStackWidgetSignal
from MySignals import myPassSelectGraphSignal


def getRandomColor():
    min_value = 64  # 设置红、绿、蓝分量的最小值，避免过暗的颜色
    red = random.randint(min_value, 255)
    green = random.randint(min_value, 255)
    blue = random.randint(min_value, 255)
    alpha = 255  # 设置不透明度为255，即完全不透明
    color = QColor(red, green, blue, alpha)
    return color


class MyNeo4jRelationItem(QGraphicsLineItem):
    def __init__(self, node1, node2):
        center1 = node1.boundingRect().center()
        center2 = node2.boundingRect().center()
        super().__init__(center1.x(), center1.y(), center2.x(), center2.y())
        self.setPen(QPen(Qt.black, 4))
        self.setZValue(-1)


class MyNeo4jNodeItem(QGraphicsEllipseItem):
    minRadios = 80
    maxRadios = 120

    def __init__(self, x, y, text, r=None):
        self.radios = random.randint(self.minRadios, self.maxRadios) if r is None else r
        super().__init__(x, y, self.radios, self.radios)
        self.setPen(QPen(getRandomColor(), 4))
        self.setBrush(getRandomColor())
        self.text = QGraphicsTextItem(text)
        center = self.boundingRect().center()
        loc = QPointF(center.x() - self.text.boundingRect().width() / 2,
                      center.y() - self.text.boundingRect().height() / 2)
        self.text.setPos(loc)

    # def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
    #     myNodeResultSignal.myNodeResultSignal.emit(self.text.toPlainText())
    #     myChangeStackWidgetSignal.myChangeStackWidgetSignal.emit(AppInfo.SUB_WINDOW.NODE_RESULT)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: typing.Optional[QWidget] = None):
        super().paint(painter, option, widget)


class MyNeo4jView(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing)
        self.setScene(QGraphicsScene())
        self.relations = {}
        # self.scene().setBackgroundBrush(getRandomColor())
        # t1 = MyNeo4jNodeItem(50, 50, '计算机组成')
        # self.__addNode(t1)
        # t2 = MyNeo4jNodeItem(150, 150, '操作系统')
        # self.__addNode(t2)
        # self.scene().addItem(MyNeo4jRelationItem(t1, t2))
        self.viewport().installEventFilter(self)
        self.nodeLocation = []
        self.nodes = {}
        self.neo4jConnect = GraphDatabase.driver(uri=AppInfo.Neo4jInfo.url, auth=AppInfo.Neo4jInfo.auth)
        myPassSelectGraphSignal.myPassSelectGraphSignal.connect(self.__receiveNeo4jName)

    def __receiveNeo4jName(self, name):
        print('received : ' + name)
        self.neo4jLabelName = name
        self.scene().clear()
        self.nodes.clear()
        self.nodeLocation.clear()
        self.relations.clear()
        self.scene().setBackgroundBrush(getRandomColor())
        with self.neo4jConnect.session() as conn:

            nodes = conn.run('MATCH (n:%s) RETURN n;' % name)
            nodes = [t['n']._properties['name'] for t in nodes]
            self.__drawNodes(nodes)

    def addNode(self, nodeName, isNewlyAdd=None):
        x, y = self.__produceNodePosition()
        node = MyNeo4jNodeItem(x, y, nodeName)
        self.__addNode(node)
        relation = MyNeo4jRelationItem(node, self.nodes['计算机科学与技术'][0])
        self.relations.update({nodeName: relation})
        self.scene().addItem(relation)
        if isNewlyAdd is not None:
            if not isNewlyAdd:
                return
            with self.neo4jConnect.session() as session:
                session.run(
                    "MERGE (t1:user%s {name:'%s'}) MERGE (t2:user%s {name:\'计算机科学与技术\'}) MERGE (t1)-[:rel%s]->(t2)" % (
                        self.neo4jLabelName, nodeName,
                        self.neo4jLabelName, self.neo4jLabelName))

    def delNode(self, nodeName):
        node = self.nodes[nodeName]
        relation = self.relations[nodeName]
        self.scene().removeItem(node[0])
        self.scene().removeItem(node[1])
        self.scene().removeItem(relation)
        del self.nodes[nodeName]
        del self.relations[nodeName]
        with self.neo4jConnect.session() as session:
            session.run("MATCH (n:user%s {name:'%s'}) detach delete n;" % (self.neo4jLabelName, nodeName))

    def __drawNodes(self, nodes):
        mainNode = (40, 40)
        self.nodeLocation.append(mainNode)
        node = MyNeo4jNodeItem(mainNode[0], mainNode[1], '计算机科学与技术', 150)
        self.__addNode(node)
        for nodeName in nodes:
            if nodeName == '计算机科学与技术':
                continue
            self.addNode(nodeName)

    def __produceNodePosition(self):
        while True:
            angle = random.uniform(0, 2 * math.pi)
            r = random.uniform(200, 300)
            x = self.nodeLocation[0][0] + (r * math.cos(angle))
            y = self.nodeLocation[0][1] + (r * math.sin(angle))
            if self.__isPositionOk((x, y)):
                self.nodeLocation.append((x, y))
                return x, y

    def __isPositionOk(self, pos):
        for t in self.nodeLocation:
            if ((t[0] - pos[0]) ** 2 + (t[1] - pos[1]) ** 2) < 30000:
                return False
        return True

    def __addNode(self, node):
        self.scene().addItem(node)
        self.scene().addItem(node.text)
        self.nodes.update({node.text.toPlainText(): (node, node.text)})

    def eventFilter(self, obj, event):
        if obj == self.viewport() and event.type() == QEvent.Type.MouseButtonPress:
            pos = event.pos()
            item = self.scene().itemAt(self.mapToScene(pos), self.transform())

            if isinstance(item, MyNeo4jNodeItem):
                if item.text.toPlainText() == '计算机科学与技术':
                    return super().eventFilter(obj, event)
                # print('Touched')
                myNodeResultSignal.myNodeResultSignal.emit(item.text.toPlainText())
                myChangeStackWidgetSignal.myChangeStackWidgetSignal.emit(AppInfo.SUB_WINDOW.NODE_RESULT.value)
            elif isinstance(item, QGraphicsTextItem):
                if item.toPlainText() == '计算机科学与技术':
                    return super().eventFilter(obj, event)
                myNodeResultSignal.myNodeResultSignal.emit(item.toPlainText())
                myChangeStackWidgetSignal.myChangeStackWidgetSignal.emit(AppInfo.SUB_WINDOW.NODE_RESULT.value)
                # print('Not Touched')
        return super().eventFilter(obj, event)
