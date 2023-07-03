# coding: utf-8
"""
Name        :cleanup_featureClasses_v200.py
Purpose     :3D都市モデル File Geodatabase から、レコード数が0のフィーチャクラスを削除する
             
Arguments   :引数1=ワークスペース
Author      :
Copyright   :
Created     :2023/06/30
Last Updated:
ArcGIS Version: ArcGIS Pro 3.1 以上
"""
# FGDB内でレコード数が0のフィーチャクラスを削除する
import arcpy
import os
import traceback

def main():
    try:
        arcpy.AddMessage(u"処理開始：")
        ws = arcpy.GetParameterAsText(0) #r""
        arcpy.env.workspace = ws
        fcs = arcpy.ListFeatureClasses()
        for fc in fcs:
            if int(arcpy.GetCount_management(fc)[0]) == 0:
                arcpy.AddMessage(u"{0} を削除します".format(fc))
                arcpy.Delete_management(fc)
            
        arcpy.AddMessage(u"処理終了：")
    except arcpy.ExecuteError:
        arcpy.AddError(arcpy.GetMessages(2))
    except Exception as e:
        err = e.args[0]
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(err)
        arcpy.AddError(pymsg)

if __name__ == '__main__':
    main()

