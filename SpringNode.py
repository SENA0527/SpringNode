# -*- coding: utf-8 -*-
import maya.api.OpenMaya as OpenMaya
import sys
import math

# プラグインの名前（ノードを呼ぶ際の名前）
kPluginNodeName = 'SpringNode'

# プラグインユニークID
CNodeId = OpenMaya.MTypeId(0x80008)###ユニークIDを入れる

# 必須
def maya_useNewAPI():
    pass

class SpringNode(OpenMaya.MPxNode):

    # キャッシュ用のメンバ変数
    cashvec = OpenMaya.MVector()
    respovec = OpenMaya.MVector()

    def __init__(self):
        OpenMaya.MPxNode.__init__(self)

    # 内部処理
    def compute(self, plug, dataBlock):

        if(plug == SpringNode.outpos):

            # 各アトリビュートのデータを取得
            inposHandle = dataBlock.inputValue(SpringNode.inpos)
            folHandle = dataBlock.inputValue(SpringNode.fol)
            resHandle = dataBlock.inputValue(SpringNode.res)
            
            outposHandle = dataBlock.outputValue(SpringNode.outpos)
            
            # 揺れ幅や追従率を変更する値
            fol = folHandle.asFloat()
            res = folHandle.asFloat()
            
            nowvec = OpenMaya.MVector(inposHandle.asFloat3())

            # 計算式
            union = ((nowvec - self.cashvec) * fol) * res + self.respovec * (1.0-res)
            result = union   + self.cashvec
            
            # メンバ変数にデータをセット
            self.cashvec = OpenMaya.MVector(result[0],result[1],result[2])
            self.respovec = OpenMaya.MVector(union[0],union[1],union[2])
            
            # プラグにデータをセット
            outposHandle.set3Float(result[0],result[1],result[2])
            
            
def cmdCreator():
    return SpringNode()
    
def nodeInitializer():

    # アトリビュートの設定

    nAttr = OpenMaya.MFnNumericAttribute()
    
    # 入力
    SpringNode.inpos = nAttr.create('in', 'in', OpenMaya.MFnNumericData.k3Float)
    nAttr.writable = True
    nAttr.keyable = True

    # follow
    SpringNode.fol = nAttr.create('fol', 'fo', OpenMaya.MFnNumericData.kFloat,0.10)
    nAttr.writable = True
    nAttr.keyable = True
    
    #respo
    SpringNode.res = nAttr.create('res', 're', OpenMaya.MFnNumericData.kFloat,0.10)
    nAttr.writable = True
    nAttr.keyable = True
    
    # 出力
    SpringNode.outpos = nAttr.create('out', 'out', OpenMaya.MFnNumericData.k3Float)
    nAttr.writable = False
    nAttr.writable = True
    
    # キャッシュ
    """SpringNode.cash = nAttr.create('cash', 'cha', OpenMaya.MFnNumericData.k3Float)
    nAttr.writable = False
    nAttr.writable = True
    
    # respo
    SpringNode.respo = nAttr.create('respo', 'resp', OpenMaya.MFnNumericData.k3Float)
    nAttr.writable = False
    nAttr.writable = True"""
    
    
    # アトリビュートをノードにセット
    SpringNode.addAttribute(SpringNode.inpos)
    SpringNode.addAttribute(SpringNode.outpos)
    SpringNode.addAttribute(SpringNode.fol)
    SpringNode.addAttribute(SpringNode.res)
    #SpringNode.addAttribute(SpringNode.cash)
    #SpringNode.addAttribute(SpringNode.respo)
    
    # アトリビュートが変更された際、指定したアトリビュートに影響を与える
    SpringNode.attributeAffects(SpringNode.inpos , SpringNode.outpos)
    SpringNode.attributeAffects(SpringNode.fol , SpringNode.outpos)
    SpringNode.attributeAffects(SpringNode.res , SpringNode.outpos)
    
# ロード処理
def initializePlugin(mobject):
    mplugin = OpenMaya.MFnPlugin(mobject)
    try:
        mplugin.registerNode(kPluginNodeName, CNodeId, cmdCreator, nodeInitializer) 
    except:
        sys.stderr.write('Failed to register node: %s' % kPluginNodeName)
        raise
        
# アンロード処理
def uninitializePlugin(mobject):
    mplugin = OpenMaya.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(CNodeId)
    except:
        sys.stderr.write('Failed to deregister node: %s' % kPluginNodeName)
        raise