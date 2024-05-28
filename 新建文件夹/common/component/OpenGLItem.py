from PySide6.QtCore import Signal, Property
from PySide6.QtGui import QOpenGLFunctions, Qt
from PySide6.QtOpenGL import QOpenGLShaderProgram, QOpenGLShader, QOpenGLFramebufferObjectFormat, \
    QOpenGLFramebufferObject
from PySide6.QtQuick import QQuickFramebufferObject
from PySide6 import QtOpenGL
from OpenGL.GL import *


class OpenGLItem(QQuickFramebufferObject, QOpenGLFunctions):
    tChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._t = 0
        self.setMirrorVertically(True)
        self.startTimer(10)

    @Property(float, notify=tChanged)
    def t(self) -> float:
        return self._t

    @t.setter
    def t(self, value: float):
        self._t = value
        self.tChanged.emit(value)

    def createRenderer(self):
        print('33333333333333')
        return FBORenderer(self)

    def timerEvent(self, event):
        self.update()


class FBORenderer(QQuickFramebufferObject.Renderer, QOpenGLFunctions):
    def __init__(self, item: OpenGLItem):
        super().__init__()

        self.program: QOpenGLShaderProgram = QOpenGLShaderProgram()

        self.item = item
        print('4444444444444444')
        #self.initializeOpenGLFunctions()
        print('555555555')


        self.program.addCacheableShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Vertex,
                                                      "attribute highp vec4 vertices;"
                                                      "varying highp vec2 coords;"
                                                      "void main() {    gl_Position = vertices;"
                                                      "    coords = vertices.xy;}")
        self.program.addCacheableShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Fragment,
                                                      "uniform lowp float t;varying highp vec2 coords;"
                                                      "void main() {"
                                                      "    lowp float i = 1. - (pow(abs(coords.x), 4.) + pow(abs(coords.y), 4.));"
                                                      "    i = smoothstep(t - 0.8, t + 0.8, i);"
                                                      "    i = floor(i * 20.) / 20.;"
                                                      "    gl_FragColor = vec4(coords * .5 + .5, i, i);}")

        print('55555555')
        self.program.bindAttributeLocation("vertices", 0)
        self.program.link()

    def render(self):
        print('22222222222222')
        pixelRatio=self.item.window().devicePixelRatio()
        self.glClearColor(0,0,0,0)
        self.glEnable(GL_DEPTH_TEST)
        self.glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.program.bind()
        self.program.enableAttributeArray(0)
        values=[-1,-1,1,-1,-1,1,1,1]
        self.glBindBuffer(GL_ARRAY_BUFFER,0)
        self.program.setAttributeArray(0,values,2)

        self.glViewport(0,0,round(self.item.width()*pixelRatio),round(self.item.height()*pixelRatio))
        self.glDisable(GL_DEPTH_TEST)
        self.glEnable(GL_BLEND)
        self.glBlendFunc(GL_SRC_ALPHA,GL_ONE)
        self.glDrawArrays(GL_TRIANGLE_STRIP,0,4)
        self.program.disableAttributeArray(0)
        self.program.release()
    def createFramebufferObject(self, size)->QOpenGLFramebufferObject:
        print('111111111111111')
        format = QOpenGLFramebufferObjectFormat()
        format.setAttachment(QOpenGLFramebufferObject.Attachment.CombinedDepthStencil)
        format.setSamples(4)
        return QOpenGLFramebufferObject(size, format)
