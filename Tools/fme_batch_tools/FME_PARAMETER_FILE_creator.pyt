# -*- coding: utf-8 -*-
"""
Name        :FME_PARAMETER_FILE_creator.pyt
Purpose     :スタンドアロンのFME.exe で変換を行うためのパラメータファイルを作成するジオプロセシング ツールボックスです
Author      :
Copyright   :
Created     :2023/07/11
Last Updated:
ArcGIS Version: ArcGIS Pro 3.1 以上
"""
import arcpy
import os
import sys
import glob
import winreg
import inspect

#
# v1.x の[Create_FME_PARAMETER_FILE.py]　から移植してクラス化
#
class FmeParameterCreater:

    PARAM1_SOURCE_DATASET=r"--SourceDataset_CITYGML"
    PARAM2_TEMPLATE_XML=r"--TEMPLATEFILE_GEODATABASE_FILE"
    PARAM3_DEST_DATASET=r"--DestDataset_GEODATABASE_FILE"
    PARAM4_ADE_XSD=r"--ADE_XSD_DOC_CITYGML"

    #FME_EXE_PATH=r"C:\Program Files\ArcGIS\Data Interoperability for ArcGIS Pro\fme.exe"
    PARAM_PARAMETER_FILE=r"PARAMETER_FILE"

    #model,gdb_schemaの設定情報
    #バージョン変更時にはファイル名を変更必要（ XXXX_v23_v2xx ）
    FMW_MODEL_DIR=r"model"
    FMW_BLDG_FILE=r"bldg_plateau_v23_v200.fmw" #建築物
    FMW_WTR_FILE=r"wtr_plateau_v23_v210.fmw" #災害リスク（洪水）
    FMW_DEM_FILE=r"dem_plateau_v23_v210.fmw" #地形
    
    GDB_SCHEMA_DIR=r"gdb_schema"
    SCHEMA_BLDG_FILE=r"bldg_plateau_v23_v210.xml" #建築物
    SCHEMA_FLD_FILE=r"fld_plateau_v23_v210.xml" #洪水
    SCHEMA_HTD_FILE=r"htd_plateau_v23_v210.xml" #高潮
    SCHEMA_IFLD_FILE=r"ifld_plateau_v23_v210.xml" #内水
    SCHEMA_TNM_FILE=r"tnm_plateau_v23_v210.xml" #津波
    SCHEMA_DEM_FILE=r"dem_plateau_v23_v210.xml" #地形
    
    @staticmethod
    def getArcGISPro_InstallDir():
        '''
        レジストリからArcGIS Pro の InstallDir を取得
        '''
        pro_path = ""
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\ESRI\ArcGISPro", 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY ) as key:
            pro_path = winreg.QueryValueEx(key, "InstallDir")[0]
        return pro_path

    @staticmethod
    def getDataInterop_InstallDir():
        '''
        レジストリからData Interoperability for ArcGIS Pro の InstallDir を取得
        '''
        interop_path = ""
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\ESRI\Data Interoperability for ArcGIS Pro", 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY ) as key:
            interop_path = winreg.QueryValueEx(key, "InstallDir")[0]
        return interop_path

    @staticmethod
    def createMultipleDatasetPath(files):
        '''
        Helpの説明にあるように
        ダブルクオートとバックスラッシュと入れた複数ファイルを指定するパラメータを作成
        '''
        sfiles = ""
        cnt = 0
        for f in files:
            cnt += 1
            if cnt == 1:
                sfiles += "\\\"{}\\\"".format(f)
            else:
                sfiles += " \\\"{}\\\"".format(f)
        sfiles = "\\\"{}\\\"".format(sfiles)
        return sfiles

    @staticmethod
    def createParameterFile(fmw_model, citygml_folders, schema_xml, output_gdb, param_file, xsd_file):
        '''
        >fme.exe PARAMETER_FILE <parameterFile>
        での実行用にparameterFile　を作成する
        '''
        blResult = True
        try:
            param0 = "\"{0}\"".format(fmw_model)
            param2 = "{0} \"{1}\"".format(FmeParameterCreater.PARAM2_TEMPLATE_XML, schema_xml)
            param3 = "{0} \"{1}\"".format(FmeParameterCreater.PARAM3_DEST_DATASET, output_gdb)
            param4 = "{0} \"{1}\"".format(FmeParameterCreater.PARAM4_ADE_XSD, xsd_file)
            #単独フォルダ：
            #files = glob.glob(citygml_folder + os.path.sep + "*.gml")
            #files_param = createMultipleDatasetPath(files)
            #複数フォルダ：
            folders = citygml_folders.split(";")
            fileslist = []
            for folder in folders:
                files = glob.glob(folder + os.path.sep + "*.gml")
                fileslist.extend(files)
            files_param = FmeParameterCreater.createMultipleDatasetPath(fileslist)
            param1 = "{0} \"{1}\"".format(FmeParameterCreater.PARAM1_SOURCE_DATASET, files_param)
            
            params = "{0} {1} {2} {3}".format(param0, param1, param2, param3)
            #v118用にiur1.4のxsdスキーマファイルを指定
            if xsd_file is not None:
                params = "{0} {1} {2} {3} {4}".format(param0, param1, param2, param3, param4)
                
            with open(param_file, 'w', encoding='shift_jis') as f:
                f.write(params)
        except Exception as e:
            arcpy.AddError(e.args[0])
            blResult = False
        return blResult

    @staticmethod
    def getBatchTools_Dir():
        local_path = os.path.abspath(os.path.dirname(__file__)) #fme_batch_tools
        return local_path

    @staticmethod
    def getConversionTools_Dir():
        local_path = os.path.abspath(os.path.dirname(__file__)) #fme_batch_tools
        parent_path = os.path.split(local_path)[0] #3D_CityModel_ConversionTools_v2
        return parent_path

# 
# ツールボックスの定義
# template:
# https://pro.arcgis.com/ja/pro-app/latest/arcpy/geoprocessing_and_python/a-template-for-python-toolboxes.htm
class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "FME のPARAMETER　FILE 作成ツールボックス"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [BldParamCreatorTool ,WtrParamCreatorTool ,DemParamCreatorTool]

# 
# 各ツールの定義
# 
class BldParamCreatorTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "FME_PARAMETER_FILE 作成ツール v2 for 建築物"
        self.description = "スタンドアロンのFME.exe で変換を行うためのパラメータファイルを作成するツールです"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # 
        # param0 [model] フォルダー下のワークベンチ
        # param1 [gdb_schema] フォルダー下の Template XML Workspace Document
        # param2 [udx] フォルダー下のCityGML ファイルが格納されているフォルダー（複数フォルダーを指定可能）
        # param3 3D都市モデル File Geodatabase（出力先）
        # param4 FME.exe 実行用のPARAMETER_FILE（ファイル名は任意）
        # 
        parent_path = FmeParameterCreater.getConversionTools_Dir() #3D_CityModel_ConversionTools_v2
        
        param0 = arcpy.Parameter(
            displayName="[model] フォルダー下のワークベンチ (bldg_plateau_v23_v2XX.fmw) :",
            name="fmw_model",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")
        param0.value = os.path.join(parent_path, os.path.join(FmeParameterCreater.FMW_MODEL_DIR, FmeParameterCreater.FMW_BLDG_FILE))  

        param1 = arcpy.Parameter(
            displayName="[gdb_schema] フォルダー下の Template XML Workspace Document (bldg_plateau_v23_v2XX.xml):",
            name="schema_xml",
            datatype="GPString", #"DEFile",
            parameterType="Required",
            direction="Input")
        #災害リスク（洪水）とUIを統一するため建築物も一覧から選択できるようにfilter.list に設定に変更
        schema_xml_1 = os.path.join(parent_path, os.path.join(FmeParameterCreater.GDB_SCHEMA_DIR, FmeParameterCreater.SCHEMA_BLDG_FILE))
        param1.filter.list = [schema_xml_1]
        param1.value = schema_xml_1 # デフォルトを設定

        param2 = arcpy.Parameter(
            displayName="[udx] フォルダー下の変換対象地物の CityGML ファイルが格納されているフォルダー（複数指定可能）:",
            name="citygml_folder",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        param3 = arcpy.Parameter(
            displayName="3D都市モデル File Geodatabase（出力先）:",
            name="output_gdb",
            datatype="DEWorkspace", 
            parameterType="Required",
            direction="Input")

        param4 = arcpy.Parameter(
            displayName="FME.exe 実行用の PARAMETER_FILE （ファイル名は任意）:",
            name="param_file",
            datatype="DEFile", 
            parameterType="Required",
            direction="Output")
        params = [param0, param1, param2, param3, param4]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        try:
            arcpy.AddMessage(u"PARAMETER_FILEの作成開始：")
            
            #FMW のモデル
            fmw_model = parameters[0].valueAsText #"bldg_plateau_v23_v200.fmw"
            
            #テンプレートGDBスキーマファイル
            schema_xml =  parameters[1].valueAsText #"bldg_plateau_v23_v200.xml"
            
            #変換するCityGMLが入っているフォルダ
            #水害や23区の対応のために複数フォルダを指定できるようにする
            citygml_folders = parameters[2].valueAsText #"02208_mutsu-shi_2022_citygml_1_op\udx\bldg" 
            
            #出力する3D都市モデルのFGDB
            output_gdb = parameters[3].valueAsText #"02208_mutsu-shi_batch_bldg.gdb" 
            
            #出力するパラメータファイル
            param_file = parameters[4].valueAsText #"ConvBuilding.par"
            
            #v118用にiur1.4のxsdスキーマファイルを指定
            xsd_file = None
            #if arcpy.GetArgumentCount() == 6:
            #    xsd_file = arcpy.GetParameterAsText(5)
            
            #チェック
            
            #パラメータファイルの中身を作成

            
            #パラメータファイルをSJISファイルとして保存
            blResult = FmeParameterCreater.createParameterFile(fmw_model, citygml_folders, schema_xml, output_gdb, param_file, xsd_file)      

            if blResult:
                arcpy.AddMessage(u"PARAMETER_FILEの作成終了")
                # パラメータファイルを指定したコマンドを作成
                FME_EXE_PATH = os.path.join(FmeParameterCreater.getDataInterop_InstallDir(), "fme.exe")
                cmd = "\"{0}\" {1} \"{2}\"".format(FME_EXE_PATH, FmeParameterCreater.PARAM_PARAMETER_FILE, param_file)
                arcpy.AddMessage(u"次の実行コマンドで実行してください: {0}".format(cmd))

            arcpy.AddMessage(u"処理終了：")
        except arcpy.ExecuteError:
            arcpy.AddError(arcpy.GetMessages(2))
        except Exception as e:
            arcpy.AddError(e.args[0])
        
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return

class WtrParamCreatorTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "FME_PARAMETER_FILE 作成ツール v2 for 災害リスク（洪水）"
        self.description = "スタンドアロンのFME.exe で変換を行うためのパラメータファイルを作成するツールです"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # 
        # param0 [model] フォルダー下のワークベンチ
        # param1 [gdb_schema] フォルダー下の Template XML Workspace Document
        # param2 [udx] フォルダー下のCityGML ファイルが格納されているフォルダー（複数フォルダーを指定可能）
        # param3 3D都市モデル File Geodatabase（出力先）
        # param4 FME.exe 実行用のPARAMETER_FILE（ファイル名は任意）
        # 
        parent_path = FmeParameterCreater.getConversionTools_Dir() #3D_CityModel_ConversionTools_v2
        
        param0 = arcpy.Parameter(
            displayName="[model] フォルダー下のワークベンチ (wtr_plateau_v23_v2XX.fmw) :",
            name="fmw_model",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")
        param0.value = os.path.join(parent_path, os.path.join(FmeParameterCreater.FMW_MODEL_DIR, FmeParameterCreater.FMW_WTR_FILE))
        
        param1 = arcpy.Parameter(
            displayName="[gdb_schema] フォルダー下の Template XML Workspace Document (fld_plateau_v23_v2XX.xml or tnm_plateau_v23_v2XX.xml or htd_plateau_v23_v2XX.xml or ifld_plateau_v23_v2XX.xml):",
            name="schema_xml",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        #各XMLファイルを一覧から選択できるようにfilter.list に設定
        schema_xml_1 = os.path.join(parent_path, os.path.join(FmeParameterCreater.GDB_SCHEMA_DIR, FmeParameterCreater.SCHEMA_FLD_FILE))
        schema_xml_2 = os.path.join(parent_path, os.path.join(FmeParameterCreater.GDB_SCHEMA_DIR, FmeParameterCreater.SCHEMA_TNM_FILE))
        schema_xml_3 = os.path.join(parent_path, os.path.join(FmeParameterCreater.GDB_SCHEMA_DIR, FmeParameterCreater.SCHEMA_HTD_FILE))
        schema_xml_4 = os.path.join(parent_path, os.path.join(FmeParameterCreater.GDB_SCHEMA_DIR, FmeParameterCreater.SCHEMA_IFLD_FILE))
        param1.filter.list = [schema_xml_1, schema_xml_2, schema_xml_3, schema_xml_4]
        param1.value = schema_xml_1 # デフォルトを洪水に設定
        
        param2 = arcpy.Parameter(
            displayName="[udx] フォルダー下の変換対象地物の CityGML ファイルが格納されているフォルダー（複数指定可能）:",
            name="citygml_folder",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input",
            multiValue=True)
        
        param3 = arcpy.Parameter(
            displayName="3D都市モデル File Geodatabase（出力先）:",
            name="output_gdb",
            datatype="DEWorkspace", 
            parameterType="Required",
            direction="Input")
        
        param4 = arcpy.Parameter(
            displayName="FME.exe 実行用の PARAMETER_FILE （ファイル名は任意）:",
            name="param_file",
            datatype="DEFile", 
            parameterType="Required",
            direction="Output")
        
        params = [param0, param1, param2, param3, param4]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        try:
            arcpy.AddMessage(u"PARAMETER_FILEの作成開始：")
            
            #FMW のモデル
            fmw_model = parameters[0].valueAsText #"bldg_plateau_v23_v200.fmw"
            
            #テンプレートGDBスキーマファイル
            schema_xml =  parameters[1].valueAsText #"bldg_plateau_v23_v200.xml"
            
            #変換するCityGMLが入っているフォルダ
            #水害や23区の対応のために複数フォルダを指定できるようにする
            citygml_folders = parameters[2].valueAsText #"02208_mutsu-shi_2022_citygml_1_op\udx\bldg" 
            
            #出力する3D都市モデルのFGDB
            output_gdb = parameters[3].valueAsText #"02208_mutsu-shi_batch_bldg.gdb" 
            
            #出力するパラメータファイル
            param_file = parameters[4].valueAsText #"ConvBuilding.par"
            
            #v118用にiur1.4のxsdスキーマファイルを指定
            xsd_file = None
            #if arcpy.GetArgumentCount() == 6:
            #    xsd_file = arcpy.GetParameterAsText(5)
            
            #チェック
            
            #パラメータファイルの中身を作成
            
            #パラメータファイルをSJISファイルとして保存
            blResult = FmeParameterCreater.createParameterFile(fmw_model, citygml_folders, schema_xml, output_gdb, param_file, xsd_file)      

            if blResult:
                arcpy.AddMessage(u"PARAMETER_FILEの作成終了")
                # パラメータファイルを指定したコマンドを作成
                FME_EXE_PATH = os.path.join(FmeParameterCreater.getDataInterop_InstallDir(), "fme.exe")
                cmd = "\"{0}\" {1} \"{2}\"".format(FME_EXE_PATH, FmeParameterCreater.PARAM_PARAMETER_FILE, param_file)
                arcpy.AddMessage(u"次の実行コマンドで実行してください: {0}".format(cmd))

            arcpy.AddMessage(u"処理終了：")
        except arcpy.ExecuteError:
            arcpy.AddError(arcpy.GetMessages(2))
        except Exception as e:
            arcpy.AddError(e.args[0])
        
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
        
class DemParamCreatorTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "FME_PARAMETER_FILE 作成ツール v2 for 地形"
        self.description = "スタンドアロンのFME.exe で変換を行うためのパラメータファイルを作成するツールです"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # 
        # param0 [model] フォルダー下のワークベンチ
        # param1 [gdb_schema] フォルダー下の Template XML Workspace Document
        # param2 [udx] フォルダー下のCityGML ファイルが格納されているフォルダー（複数フォルダーを指定可能）
        # param3 3D都市モデル File Geodatabase（出力先）
        # param4 FME.exe 実行用のPARAMETER_FILE（ファイル名は任意）
        # 
        parent_path = FmeParameterCreater.getConversionTools_Dir() #3D_CityModel_ConversionTools_v2
        
        param0 = arcpy.Parameter(
            displayName="[model] フォルダー下のワークベンチ (dem_plateau_v23_v2XX.fmw) :",
            name="fmw_model",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")
        param0.value = os.path.join(parent_path, os.path.join(FmeParameterCreater.FMW_MODEL_DIR, FmeParameterCreater.FMW_DEM_FILE))  

        param1 = arcpy.Parameter(
            displayName="[gdb_schema] フォルダー下の Template XML Workspace Document (dem_plateau_v23_v2XX.xml):",
            name="schema_xml",
            datatype="GPString", #"DEFile",
            parameterType="Required",
            direction="Input")
        #災害リスク（洪水）とUIを統一するため建築物も一覧から選択できるようにfilter.list に設定に変更
        schema_xml_1 = os.path.join(parent_path, os.path.join(FmeParameterCreater.GDB_SCHEMA_DIR, FmeParameterCreater.SCHEMA_DEM_FILE))
        param1.filter.list = [schema_xml_1]
        param1.value = schema_xml_1 # デフォルトを設定

        param2 = arcpy.Parameter(
            displayName="[udx] フォルダー下の変換対象地物の CityGML ファイルが格納されているフォルダー（複数指定可能）:",
            name="citygml_folder",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        param3 = arcpy.Parameter(
            displayName="3D都市モデル File Geodatabase（出力先）:",
            name="output_gdb",
            datatype="DEWorkspace", 
            parameterType="Required",
            direction="Input")

        param4 = arcpy.Parameter(
            displayName="FME.exe 実行用の PARAMETER_FILE （ファイル名は任意）:",
            name="param_file",
            datatype="DEFile", 
            parameterType="Required",
            direction="Output")
        params = [param0, param1, param2, param3, param4]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        try:
            arcpy.AddMessage(u"PARAMETER_FILEの作成開始：")
            
            #FMW のモデル
            fmw_model = parameters[0].valueAsText #"bldg_plateau_v23_v200.fmw"
            
            #テンプレートGDBスキーマファイル
            schema_xml =  parameters[1].valueAsText #"bldg_plateau_v23_v200.xml"
            
            #変換するCityGMLが入っているフォルダ
            #水害や23区の対応のために複数フォルダを指定できるようにする
            citygml_folders = parameters[2].valueAsText #"02208_mutsu-shi_2022_citygml_1_op\udx\bldg" 
            
            #出力する3D都市モデルのFGDB
            output_gdb = parameters[3].valueAsText #"02208_mutsu-shi_batch_bldg.gdb" 
            
            #出力するパラメータファイル
            param_file = parameters[4].valueAsText #"ConvBuilding.par"
            
            #v118用にiur1.4のxsdスキーマファイルを指定
            xsd_file = None
            #if arcpy.GetArgumentCount() == 6:
            #    xsd_file = arcpy.GetParameterAsText(5)
            
            #チェック
            
            #パラメータファイルの中身を作成

            
            #パラメータファイルをSJISファイルとして保存
            blResult = FmeParameterCreater.createParameterFile(fmw_model, citygml_folders, schema_xml, output_gdb, param_file, xsd_file)      

            if blResult:
                arcpy.AddMessage(u"PARAMETER_FILEの作成終了")
                # パラメータファイルを指定したコマンドを作成
                FME_EXE_PATH = os.path.join(FmeParameterCreater.getDataInterop_InstallDir(), "fme.exe")
                cmd = "\"{0}\" {1} \"{2}\"".format(FME_EXE_PATH, FmeParameterCreater.PARAM_PARAMETER_FILE, param_file)
                arcpy.AddMessage(u"次の実行コマンドで実行してください: {0}".format(cmd))

            arcpy.AddMessage(u"処理終了：")
        except arcpy.ExecuteError:
            arcpy.AddError(arcpy.GetMessages(2))
        except Exception as e:
            arcpy.AddError(e.args[0])
        
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
