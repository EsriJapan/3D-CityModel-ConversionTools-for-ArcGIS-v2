# coding : utf-8
"""
Name        :create_setup_domain_field_v200.py
Purpose     :各都市毎に設定するコード値ドメインを設定するスクリプト
             
argument    :引数1=フォルダパス、引数2=ワークスペース
Author      :
Copyright   :
Created     :2023/06/30
Last Updated:2023/08/04
ArcGIS Version: ArcGIS Pro 3.1 以上
"""

import arcpy
import xml.etree.ElementTree as ET
import sys
import os
import datetime
import traceback

'''
  建物用の定義
'''
# ドメイン設定対象のフィーチャ クラス
buildingTargetLayers = ["lod0_Building", "lod1_Building", "lod2_Building", "lod3_Building", "lod1_BuildingPart", "lod2_BuildingPart", "lod3_BuildingPart"]
# ドメイン作成用リスト（key:ドメイン名, description:ドメイン対象 xml ファイル）
buildingDomainList = {
            # "Building_name":"Building_name.xml", 
            "BuildingDetailAttribute_buildingStructureOrgType":"BuildingDetailAttribute_buildingStructureOrgType.xml", 
            "BuildingDetailAttribute_majorUsage": "BuildingDetailAttribute_majorUsage.xml", 
            "BuildingDetailAttribute_majorUsage2": "BuildingDetailAttribute_majorUsage2.xml",
            "BuildingDetailAttribute_orgUsage": "BuildingDetailAttribute_orgUsage.xml",
            "BuildingDetailAttribute_orgUsage2": "BuildingDetailAttribute_orgUsage2.xml",
            "BuildingDetailAttribute_detailedUsage2": "BuildingDetailAttribute_detailedUsage2.xml",
            "BuildingDetailAttribute_detailedUsage3": "BuildingDetailAttribute_detailedUsage3.xml",
            "BuildingDetailAttribute_groundFloorUsage": "BuildingDetailAttribute_groundFloorUsage.xml",
            "BuildingDetailAttribute_secondFloorUsage": "BuildingDetailAttribute_secondFloorUsage.xml",
            "BuildingDetailAttribute_thirdFloorUsage": "BuildingDetailAttribute_thirdFloorUsage.xml",
            "BuildingDetailAttribute_basementFloorUsage": "BuildingDetailAttribute_basementFloorUsage.xml",
            "BuildingDetailAttribute_basementFirstUsage": "BuildingDetailAttribute_basementFirstUsage.xml",
            "BuildingDetailAttribute_basementSecondUsage": "BuildingDetailAttribute_basementSecondUsage.xml",
            "BuildingRiverFloodingRiskAttribute_description": "BuildingRiverFloodingRiskAttribute_description.xml",
            "BuildingRiverFloodingRiskAttribute_rankOrg": "BuildingRiverFloodingRiskAttribute_rankOrg.xml",
            "BuildingTsunamiRiskAttribute_description": "BuildingTsunamiRiskAttribute_description.xml",
            "BuildingTsunamiRiskAttribute_rankOrg": "BuildingTsunamiRiskAttribute_rankOrg.xml",
            "BuildingHighTideRiskAttribute_description": "BuildingHighTideRiskAttribute_description.xml",
            "BuildingHighTideRiskAttribute_rankOrg": "BuildingHighTideRiskAttribute_rankOrg.xml",
            "BuildingInlandFloodingRiskAttribute_description": "BuildingInlandFloodingRiskAttribute_description.xml",
            "BuildingInlandFloodingRiskAttribute_rankOrg": "BuildingInlandFloodingRiskAttribute_rankOrg.xml",
            "KeyValuePairAttribute_key": "KeyValuePairAttribute_key.xml"
        }
# ドメイン設定フィールドリスト（key:フィールド名, description:ドメイン名）
setBuildingDomainList = {
           # "gml_name":"Building_name", 
           "uro_BuildingDetailAttribute_buildingStructureOrgType":"BuildingDetailAttribute_buildingStructureOrgType", 
           "uro_BuildingDetailAttribute_majorUsage": "BuildingDetailAttribute_majorUsage", 
           "uro_BuildingDetailAttribute_majorUsage2": "BuildingDetailAttribute_majorUsage2",
           "uro_BuildingDetailAttribute_orgUsage": "BuildingDetailAttribute_orgUsage",
           "uro_BuildingDetailAttribute_orgUsage2": "BuildingDetailAttribute_orgUsage2",
           "uro_BuildingDetailAttribute_detailedUsage2": "BuildingDetailAttribute_detailedUsage2",
           "uro_BuildingDetailAttribute_detailedUsage3": "BuildingDetailAttribute_detailedUsage3",
           "uro_BuildingDetailAttribute_groundFloorUsage": "BuildingDetailAttribute_groundFloorUsage",
           "uro_BuildingDetailAttribute_secondFloorUsage": "BuildingDetailAttribute_secondFloorUsage",
           "uro_BuildingDetailAttribute_thirdFloorUsage": "BuildingDetailAttribute_thirdFloorUsage",
           "uro_BuildingDetailAttribute_basementUsage": "BuildingDetailAttribute_basementFloorUsage",
           "uro_BuildingDetailAttribute_basementFirstUsage": "BuildingDetailAttribute_basementFirstUsage",
           "uro_BuildingDetailAttribute_basementSecondUsage": "BuildingDetailAttribute_basementSecondUsage",
           "uro_BuildingRiverFloodingRiskAttribute_description": "BuildingRiverFloodingRiskAttribute_description",
           "uro_BuildingRiverFloodingRiskAttribute_rankOrg": "BuildingRiverFloodingRiskAttribute_rankOrg",
           "uro_BuildingTsunamiRiskAttribute_description": "BuildingTsunamiRiskAttribute_description",
           "uro_BuildingTsunamiRiskAttribute_rankOrg": "BuildingTsunamiRiskAttribute_rankOrg",
           "uro_BuildingHighTideRiskAttribute_description": "BuildingHighTideRiskAttribute_description",
           "uro_BuildingHighTideRiskAttribute_rankOrg": "BuildingHighTideRiskAttribute_rankOrg",
           "uro_BuildingInlandFloodingRiskAttribute_description": "BuildingInlandFloodingRiskAttribute_description",
           "uro_BuildingInlandFloodingRiskAttribute_rankOrg": "BuildingInlandFloodingRiskAttribute_rankOrg",
           "uro_KeyValuePairAttribute_key1": "KeyValuePairAttribute_key",
           "uro_KeyValuePairAttribute_key2": "KeyValuePairAttribute_key",
           "uro_KeyValuePairAttribute_key3": "KeyValuePairAttribute_key",
           "uro_KeyValuePairAttribute_key4": "KeyValuePairAttribute_key",
           "uro_KeyValuePairAttribute_key5": "KeyValuePairAttribute_key",
           "uro_KeyValuePairAttribute_key6": "KeyValuePairAttribute_key",
           "uro_KeyValuePairAttribute_key7": "KeyValuePairAttribute_key",
           "uro_KeyValuePairAttribute_key8": "KeyValuePairAttribute_key",
           "uro_KeyValuePairAttribute_key9": "KeyValuePairAttribute_key",
           "uro_KeyValuePairAttribute_key10": "KeyValuePairAttribute_key",
           "uro_KeyValuePairAttribute_codeValue1": "KeyValuePairAttribute_codeValue1",
           "uro_KeyValuePairAttribute_codeValue2": "KeyValuePairAttribute_codeValue2",
           "uro_KeyValuePairAttribute_codeValue3": "KeyValuePairAttribute_codeValue3",
           "uro_KeyValuePairAttribute_codeValue4": "KeyValuePairAttribute_codeValue4",
           "uro_KeyValuePairAttribute_codeValue5": "KeyValuePairAttribute_codeValue5",
           "uro_KeyValuePairAttribute_codeValue6": "KeyValuePairAttribute_codeValue6",
           "uro_KeyValuePairAttribute_codeValue7": "KeyValuePairAttribute_codeValue7",
           "uro_KeyValuePairAttribute_codeValue8": "KeyValuePairAttribute_codeValue8",
           "uro_KeyValuePairAttribute_codeValue9": "KeyValuePairAttribute_codeValue9",
           "uro_KeyValuePairAttribute_codeValue10": "KeyValuePairAttribute_codeValue10"
}

'''
  土地利用用の定義
'''
# ドメイン設定対象のフィーチャ クラス
landuseTargetLayers = ["lod1_LandUse"]
# ドメイン作成用リスト（key:ドメイン名, description:ドメイン対象 xml ファイル）
landuseDomainList = {
            "LandUseDetailAttribute_orgLandUse": "LandUseDetailAttribute_orgLandUse.xml"
        }
# ドメイン設定フィールドリスト（key:フィールド名, description:ドメイン名）
setLanduseDomainList = {
           "uro_landUseDetailAttribute_orgLandUse": "LandUseDetailAttribute_orgLandUse"
}

'''
  水部用の定義
'''
# ドメイン設定対象のフィーチャ クラス
fldTargetLayers = ["lod1_WaterBody_fld"]
# ドメイン作成用リスト（key:ドメイン名, description:ドメイン対象 xml ファイル）
fldDomainList = {
           "WaterBody_Name": "WaterBody_name.xml",
           "WaterBodyRiverFloodingRiskAttribute_description": "WaterBodyRiverFloodingRiskAttribute_description.xml",
           "WaterBodyRiverFloodingRiskAttribute_rankOrg": "WaterBodyRiverFloodingRiskAttribute_rankOrg.xml"
        }
# ドメイン設定フィールドリスト（key:フィールド名, description:ドメイン名）
setFldDomainList = {
           "gml_name": "WaterBody_Name",
           "uro_WaterBodyRiverFloodingRiskAttribute_description": "WaterBodyRiverFloodingRiskAttribute_description",
           "uro_WaterBodyRiverFloodingRiskAttribute_rankOrg": "WaterBodyRiverFloodingRiskAttribute_rankOrg"
           }

# ドメイン設定対象のフィーチャ クラス
tnmTargetLayers = ["lod1_WaterBody_tnm"]
# ドメイン作成用リスト（key:ドメイン名, description:ドメイン対象 xml ファイル）
tnmDomainList = {
           "WaterBody_Name": "WaterBody_name.xml",
           "WaterBodyTsunamiRiskAttribute_description": "WaterBodyTsunamiRiskAttribute_description.xml",
           "WaterBodyTsunamiRiskAttribute_rankOrg": "WaterBodyTsunamiRiskAttribute_rankOrg.xml"
        }
# ドメイン設定フィールドリスト（key:フィールド名, description:ドメイン名）
setTnmDomainList = {
           "gml_name": "WaterBody_Name",
           "uro_WaterBodyTsunamiRiskAttribute_description": "WaterBodyTsunamiRiskAttribute_description",
           "uro_WaterBodyTsunamiRiskAttribute_rankOrg": "WaterBodyTsunamiRiskAttribute_rankOrg"
           }

# ドメイン設定対象のフィーチャ クラス
htdTargetLayers = ["lod1_WaterBody_htd"]
# ドメイン作成用リスト（key:ドメイン名, description:ドメイン対象 xml ファイル）
htdDomainList = {
           "WaterBody_Name": "WaterBody_name.xml",
           "WaterBodyHighTideRiskAttribute_description": "WaterBodyHighTideRiskAttribute_description.xml",
           "WaterBodyHighTideRiskAttribute_rankOrg": "WaterBodyHighTideRiskAttribute_rankOrg.xml"
        }
# ドメイン設定フィールドリスト（key:フィールド名, description:ドメイン名）
setHtdDomainList = {
           "gml_name": "WaterBody_Name",
           "uro_WaterBodyHighTideRiskAttribute_description": "WaterBodyHighTideRiskAttribute_description",
           "uro_WaterBodyHighTideRiskAttribute_rankOrg": "WaterBodyHighTideRiskAttribute_rankOrg"
           }

# ドメイン設定対象のフィーチャ クラス
ifldTargetLayers = ["lod1_WaterBody_ifld"]
# ドメイン作成用リスト（key:ドメイン名, description:ドメイン対象 xml ファイル）
ifldDomainList = {
           "WaterBody_Name": "WaterBody_name.xml",
           "WaterBodyInlandFloodingRiskAttribute_description": "WaterBodyInlandFloodingRiskAttribute_description.xml",
           "WaterBodyInlandFloodingRiskAttribute_rankOrg": "WaterBodyInlandFloodingRiskAttribute_rankOrg.xml"
        }
# ドメイン設定フィールドリスト（key:フィールド名, description:ドメイン名）
setIfldDomainList = {
           "gml_name": "WaterBody_Name",
           "uro_WaterBodyInlandFloodingRiskAttribute_description": "WaterBodyInlandFloodingRiskAttribute_description",
           "uro_WaterBodyInlandFloodingRiskAttribute_rankOrg": "WaterBodyInlandFloodingRiskAttribute_rankOrg"
           }

'''
  ドメイン説明用リスト
'''
domainDescriptionList = {
           "Building_name": "建築物を識別する名称",
           "BuildingDetailAttribute_buildingStructureOrgType": "都市ごとの独自の区分に基づく建築物の構造種別",
           "BuildingDetailAttribute_majorUsage": "urf:orgUsage よりも粗い区分による都市独自の分類",
           "BuildingDetailAttribute_majorUsage2": "uro:orgUsage よりも粗く、uro:majorUsage よりも細かい区分による都市独自の分類",
           "BuildingDetailAttribute_orgUsage": "都市計画基礎調査実施要領（国土交通省都市局）に示された建築物の「用途分類」に相当する都市独自の分類",
           "BuildingDetailAttribute_orgUsage2": "都市計画基礎調査実施要領（国土交通省都市局）に示された建築物の「用途分類」のうち、商業施設、文教厚生施設、運輸倉庫施設、工場が詳細化された区分に相当する都市独自の分類",
           "BuildingDetailAttribute_detailedUsage2": "uro:detailedUsage よりも細かい区分による都市独自の分類",
           "BuildingDetailAttribute_detailedUsage3": "uro:detailedUsage2 よりも細かい区分による都市独自の分類",
           "BuildingDetailAttribute_groundFloorUsage": "都市ごとの独自の区分に基づく建築物 1 階の用途",
           "BuildingDetailAttribute_secondFloorUsage": "都市ごとの独自の区分に基づく建築物の 2 階または 2 階以上の用途",
           "BuildingDetailAttribute_thirdFloorUsage": "都市ごとの独自の区分に基づく建築物の 3 階または 3 階以上の用途",
           "BuildingDetailAttribute_basementFloorUsage": "都市ごとの独自の区分に基づく建築物の地下の用途",
           "BuildingDetailAttribute_basementFirstUsage": "都市ごとの独自の区分に基づく建築物の地下 1 階の用途",
           "BuildingDetailAttribute_basementSecondUsage": "都市ごとの独自の区分に基づく建築物の地下 2 階の用途",
           "BuildingRiverFloodingRiskAttribute_description": "指定河川の名称",
           "BuildingRiverFloodingRiskAttribute_rankOrg": "都道府県独自に設定した浸水深の区分（河川氾濫）",
           "BuildingTsunamiRiskAttribute_description": "津波浸水想定の属性を付与する元となる図またはデ－タの名称",
           "BuildingTsunamiRiskAttribute_rankOrg": "都道府県独自に設定した浸水深の区分（津波）",
           "BuildingHighTideRiskAttribute_description": "高潮浸水想定区域の属性を付与する元となる図またはデ－タの名称",
           "BuildingHighTideRiskAttribute_rankOrg": "都道府県独自に設定した浸水深の区分（高潮）",
           "BuildingInlandFloodingRiskAttribute_description": "内水浸水想定区域の属性を付与する元となる図またはデ－タの名称",
           "BuildingInlandFloodingRiskAttribute_rankOrg": "都道府県独自に設定した浸水深の区分（内水）",
           "KeyValuePairAttribute_key": "建築物に付与する追加情報",
           "LandUseDetailAttribute_orgLandUse": "都市独自の分類による土地利用用途",
           "WaterBody_Name": "水部を識別する名称",
           "WaterBodyRiverFloodingRiskAttribute_description": "指定河川の名称",
           "WaterBodyRiverFloodingRiskAttribute_rankOrg": "都道府県独自に設定した浸水深の区分（河川氾濫）",
           "WaterBodyTsunamiRiskAttribute_description": "津波浸水想定の属性を付与する元となる図またはデ－タの名称",
           "WaterBodyTsunamiRiskAttribute_rankOrg": "都道府県独自に設定した浸水深の区分（津波）",
           "WaterBodyHighTideRiskAttribute_description": "高潮浸水想定区域の属性を付与する元となる図またはデ－タの名称",
           "WaterBodyHighTideRiskAttribute_rankOrg": "都道府県独自に設定した浸水深の区分（高潮）",
           "WaterBodyInlandFloodingRiskAttribute_description": "内水浸水想定区域の属性を付与する元となる図またはデ－タの名称",
           "WaterBodyInlandFloodingRiskAttribute_rankOrg": "都道府県独自に設定した浸水深の区分（内水）"
}

'''
  Error ハンドリング用
'''
class domainSettingException(Exception):
    pass


codeValueList = {}
settedDomainNameList = {}
setDomains = {}
setDomainList = {}

'''
  ドメイン作成およびドメイン値設定用メソッド
   - folderPath: フォルダパス
   - domainName: ドメイン名
   - domainList: 対象のドメイン作成用リスト
'''
def createDomain(folderPath, domainName, domainList):
    # XML ファイル名を設定
    fileName = domainList[domainName]
    filePath = folderPath + "\\" + fileName
    keyValueCnt = 0
    # 指定したフォルダに対象の XML ファイルがある場合のみ実行
    try:
        if os.path.isfile(filePath):
            # 同一のドメインがファイル ジオデータベースに設定されているか判定
            if domainName not in settedDomainNameList.keys():
                # ドメインが設定されていない場合、新規にドメインを作成
                arcpy.management.CreateDomain(arcpy.env.workspace, domainName, domain_description=domainDescriptionList[domainName],  field_type="TEXT")
                arcpy.AddMessage(u"[{0}]: {2} に ドメイン: {1} を新規作成しました。".format(str(datetime.datetime.now()), arcpy.env.workspace, domainName ))
                setDomains = {}
            else:
                # ドメインが定義されている場合、ドメインに設定されているコード値を取得
                setDomains = settedDomainNameList[domainName].codedValues
                arcpy.AddMessage(u"[{0}]: ドメイン: {1} は既に {2} に定義されています。".format(str(datetime.datetime.now()), domainName, arcpy.env.workspace))
            
            # ドメインにコード値を設定
            xmlFile = ET.parse(filePath)
            for dictionaryEntry in xmlFile.findall('{http://www.opengis.net/gml}dictionaryEntry'):
                for Definition in dictionaryEntry.findall('{http://www.opengis.net/gml}Definition'):
                    # xml ファイルから domainName と descritption の値を取得
                    code = Definition.find('{http://www.opengis.net/gml}name').text
                    description = Definition.find('{http://www.opengis.net/gml}description').text
                    # 対象の key がドメインに設定済みかをチェック
                    if code not in setDomains.keys():
                        # key または description が存在しない場合、不正なコードとなるため設定しない
                        if not description:
                            arcpy.AddWarning(u"[{0}]: ドメイン: {1} に追加する {2} のコードの説明がないので処理をスキップします".format(str(datetime.datetime.now()), domainName, code))
                            continue
                        # ドメイン名が 'KeyValuePairAttribute_key' の場合、key に対応する別途 xml ファイルが存在するため設定する
                        if domainName == "KeyValuePairAttribute_key":
                            keyValueCnt = keyValueCnt + 1
                            if keyValueCnt <= 10:
                                newDomainName = "KeyValuePairAttribute_codeValue" + str(keyValueCnt)
                                newDomainFile = "KeyValuePairAttribute_key" + str(code)  + ".xml"
                                codeValueList[newDomainName] = newDomainFile
                                domainDescriptionList[newDomainName] = u"uro_keyValuePairAttribute_codeValue{0}: フィールド用（{1}）".format(str(keyValueCnt), description)
                        # ドメインにコード値を設定
                        arcpy.management.AddCodedValueToDomain(arcpy.env.workspace, domainName, code, description)
                        arcpy.AddMessage(u"[{0}]: ドメイン: {1} に コード: {2}, 説明: {3} のコードを設定しました。".format(str(datetime.datetime.now()), domainName, code, description))
            domList = arcpy.da.ListDomains(arcpy.env.workspace)
            # 設定したドメインを設定済みドメイン リストに追加
            for dom in domList:
                if dom.name == domainName:
                    settedDomainNameList[domainName] = dom
        else:
            arcpy.AddWarning(u"[{0}]: {1} は定義されていないので処理をスキップします".format(str(datetime.datetime.now()), filePath))
    except arcpy.ExecuteError:
        arcpy.AddError(arcpy.GetMessages(2))
        raise domainSettingException(arcpy.ExecuteError)
    except Exception as e:
        err = e.args[0]
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(err)
        arcpy.AddError(pymsg)
        raise domainSettingException(e)

'''
    フィールドにドメインを設定
    - targetLayers: 対象のレイヤー
    - setDomainList: ドメイン設定対象のフィールド
'''
def  setFieldToDomain(targetLayers, setDomainList):
    # 2. フィールドにドメインを設定
    featureclasses = arcpy.ListFeatureClasses()
    # 構成リストのフィールドに定義情報を繰り返す
    try:
        for columnName in setDomainList:
            # ドメイン名の取得
            domainName = setDomainList[columnName]
            if domainName in settedDomainNameList.keys():
                for target in targetLayers:
                    if target in featureclasses:
                        tableview = arcpy.env.workspace + "\\" + target
                        fields = arcpy.ListFields(tableview, wild_card=columnName)
                        for field in fields:
                            # 対象のフィールドに既にドメインが設定されていない場合のみドメインを設定
                            if len(field.domain) == 0:
                                arcpy.AddMessage(u"[{0}]: フィーチャクラス: {1} の フィールド: {2} に ドメイン: {3} を設定しました。".format(str(datetime.datetime.now()), target, columnName, domainName))
                                arcpy.management.AssignDomainToField(tableview, columnName, domainName)
                            else:
                                arcpy.AddWarning(u"[{0}]: フィーチャクラス: {1} の フィールド: {2} は既にドメインが設定済みです。".format(str(datetime.datetime.now()), target, columnName))
    except Exception as e:
        raise domainSettingException(e)
    arcpy.AddMessage(u"[{0}]: メイン処理を正常終了します。".format(str(datetime.datetime.now())))


'''
   メインメソッド
    - folderPath: フォルダパス
    - fgdb: ファイル ジオデータベース
'''
def doMainEvent(folderPath, fgdb):
    arcpy.AddMessage(u"[{0}]: メイン処理を開始します。".format(str(datetime.datetime.now())))
    # ワークスペースにファイル ジオデータベースを設定
    arcpy.env.workspace = fgdb
    # ファイル ジオデータベースに設定済みのドメインを取得
    settedDomainList = arcpy.da.ListDomains(arcpy.env.workspace)
    for settedDomain in settedDomainList:
        settedDomainNameList[settedDomain.name] = settedDomain

    # ファイル ジオデータベースに存在するフィーチャ クラスを全量取得
    tables = arcpy.ListFeatureClasses(wild_card="*")
    targetLayers = []
    domainList = {}
    # 対象のファイル ジオデータベースではない場合はエラー
    if "lod0_Building" not in tables and "lod1_LandUse" not in tables and "lod1_WaterBody_fld" not in tables and "lod1_WaterBody_tnm" not in tables and "lod1_WaterBody_htd" not in tables and "lod1_WaterBody_ifld" not in tables:
        arcpy.AddError(u"[{0}]: {1} はドメイン設定対象のファイル ジオデータベースではありません。".format(str(datetime.datetime.now()), arcpy.env.workspace))
        raise ValueError("ファイル ジオデータベース設定エラー")
    
    # 1.ファイル ジオデータベースから対象の地物がある場合、ドメインの設定を行う
    if "lod0_Building" in tables:
        targetLayers = buildingTargetLayers
        domainList = buildingDomainList
        setDomainList = setBuildingDomainList
        # ドメイン作成およびドメイン値設定
        try:
            for key in domainList.keys():
                createDomain(folderPath, key, domainList)

            for key in codeValueList.keys():
                createDomain(folderPath, key, codeValueList)
            setFieldToDomain(targetLayers, setDomainList)
        except Exception as e:
            raise domainSettingException(e)
    if "lod1_LandUse" in tables:
        targetLayers = landuseTargetLayers
        domainList = landuseDomainList
        setDomainList = setLanduseDomainList
        # ドメイン作成およびドメイン値設定
        try:
            for key in domainList.keys():
                createDomain(folderPath, key, domainList)
            setFieldToDomain(targetLayers, setDomainList)
        except Exception as e:
            raise domainSettingException(e)
    if "lod1_WaterBody_fld" in tables:
        targetLayers = fldTargetLayers
        domainList = fldDomainList
        setDomainList = setFldDomainList
        # ドメイン作成およびドメイン値設定
        try:
            for key in domainList.keys():
                createDomain(folderPath, key, domainList)
            setFieldToDomain(targetLayers, setDomainList)
        except Exception as e:
            raise domainSettingException(e)
    if "lod1_WaterBody_tnm" in tables:
        targetLayers = tnmTargetLayers
        domainList = tnmDomainList
        setDomainList = setTnmDomainList
        # ドメイン作成およびドメイン値設定
        try:
            for key in domainList.keys():
                createDomain(folderPath, key, domainList)
            setFieldToDomain(targetLayers, setDomainList)
        except Exception as e:
            raise domainSettingException(e)
    if "lod1_WaterBody_htd" in tables:
        targetLayers = htdTargetLayers
        domainList = htdDomainList
        setDomainList = setHtdDomainList
        # ドメイン作成およびドメイン値設定
        try:
            for key in domainList.keys():
                createDomain(folderPath, key, domainList)
            setFieldToDomain(targetLayers, setDomainList)
        except Exception as e:
            raise domainSettingException(e)
    if "lod1_WaterBody_ifld" in tables:
        targetLayers = ifldTargetLayers
        domainList = ifldDomainList
        setDomainList =setIfldDomainList
        # ドメイン作成およびドメイン値設定
        try:
            for key in domainList.keys():
                createDomain(folderPath, key, domainList)
            setFieldToDomain(targetLayers, setDomainList)
        except Exception as e:
            raise domainSettingException(e)

    

if __name__ == '__main__':
    # 0.初期処理
    try:
        arcpy.AddMessage(u"[{0}]: 処理を開始します。".format(str(datetime.datetime.now())))
        folderPath = arcpy.GetParameterAsText(0)
        fgdb = arcpy.GetParameterAsText(1)
        arcpy.AddMessage(u"[{0}]: パラメータ1 に {1}、パラメータ2 に {2} が設定されました。".format(str(datetime.datetime.now()), folderPath, fgdb))
        doMainEvent(folderPath, fgdb)
    except:
        arcpy.AddError(u"[{0}]:処理が失敗しました。".format(str(datetime.datetime.now())))
    finally:
        arcpy.AddMessage(u"[{0}]: 処理を終了します。".format(str(datetime.datetime.now())))