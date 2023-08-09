# 3D-CityModel-ConversionTools-for-ArcGIS-v2
# 概要
「3D 都市モデルデータ変換ツール v2.0 for ArcGIS」 は、[PLATEAU](https://www.mlit.go.jp/plateau/) で整備し、G空間情報センターで公開している[3D都市モデル](https://www.geospatial.jp/ckan/dataset/plateau)（CityGML）のデータを、ArcGIS で利用可能な[ファイル ジオデータベース](https://pro.arcgis.com/ja/pro-app/latest/help/data/geodatabases/manage-file-gdb/file-geodatabases.htm) へ変換するツールです。  
本ツールで変換可能なデータは、[製品仕様書 第2.3版（3D 都市モデル標準製品仕様書 series No.01（2022/09/23 2.3 版））](https://www.mlit.go.jp/plateau/file/libraries/doc/plateau_doc_0001_ver02.pdf) に対応した 3D都市モデルです。[3D 都市モデル標準製品仕様書 series No.01（2021/03/26 1.0.0版）](https://www.mlit.go.jp/plateau/file/libraries/doc/plateau_doc_0001_ver01.pdf)のデータに対応した変換ツールは [こちら](https://github.com/EsriJapan/3D-CityModel-ConversionTools-for-ArcGIS) をご利用ください。  
本ツールは、国土交通省都市局監修のもと、ESRIジャパン株式会社にて作成・開発したものです。

  
### リリース履歴
* 2023/06/30 ： 「3D 都市モデルデータ変換ツール for ArcGIS」バージョン2.0 を公開
  
## 対応データの一覧

3D都市モデル（CityGML）の対応している地物と、変換されるファイル ジオデータベース内のフィーチャクラスの関係は、次の通りです。

|地物||対応状況|変換先のフィーチャクラス名|
|:---|:---|:---:|:---|
|建築物||〇（LOD0、1、2、3ごと分解して変換）|lod0_Building, lod1_Building, lod2_Building, lod3_Building|
||建築物部分|〇（LOD2、3ごとに分解して変換）|lod2_BuildingPart, lod3_BuildingPart|
||屋根|〇（LOD2、3ごとに分解して変換）|lod2_RoofSurface, lod3_RoofSurface|
||外壁|〇（LOD2、3ごとに分解して変換）|lod2_WallSurface, lod3_WallSurface|
||接地面|〇（LOD2、3ごとに分解して変換）|lod2_GroundSurface, lod3_GroundSurface|
||外部天井|〇|lod3_OuterCeilingSurface|
||外部床面|〇（LOD2、3ごとに分解して変換）|lod2_OuterFloorSurface, lod3_OuterFloorSurface|
||閉鎖面|〇（LOD2、3ごとに分解して変換）|lod2_ClosureSurface, lod3_ClosureSurface|
||建築物付属物|〇（LOD2、3ごとに分解して変換）|lod2_BuildingInstallation, lod3_BuildingInstallation|
||窓|〇|lod3_Window|
||扉|〇|lod3_Door|
|道路||〇（LOD0、1、2、3ごとに分解して変換）|lod0_Road, lod1_Road, lod2_Road, lod3_Road|
||通行可能領域|〇（LOD2、3ごとに分解して変換）|lod2_TrafficArea, lod3_TrafficArea|
||交通補助領域|〇（LOD2、3ごとに分解して変換）|lod2_AuxiliaryTrafficArea, lod3_AuxiliaryTrafficArea|
|地形（起伏）|TIN|〇（LOD1、2、3ごとに分解して変換）|lod1_TinRelief, lod2_TinRelief, lod3_TinRelief|
||MassPoint|〇（LOD1、2、3ごとに分解して変換）|lod1_MassPointRelief, lod2_MassPointRelief, lod3_MassPointRelief|
|土地利用||〇|lod1_LandUse|
|都市計画区域||〇||
||都市計画区域|〇|lod1_UrbanPlanningArea|
||準都市計画区域|〇|lod1_QuasiUrbanPlanningArea|
|区域区分||〇|lod1_AreaClassification|
|地域地区||〇|lod1_DistrictAndZones|
||用途地域|〇|lod1_UseDistrict|
||特別用途地区|〇|lod1_SpecialUseDistrict|
||特定用途制限地域|〇|lod1_SpecialUseRestrictionDistrict|
||特例容積率適用地区|〇|lod1_ExceptionalFloorAreaRateDistrict|
||高層住居誘導地区|〇|lod1_HighRiseResidentialAttractionDistrict|
||高度地区|〇|lod1_HeightControlDistrict|
||高度利用地区|〇|lod1_HighLevelUseDistrict|
||特定街区|〇|lod1_SpecifiedBlock|
||都市再生特別地区|〇|lod1_SpecialUrbanRenaissanceDistrict|
||居住調整地域|〇|lod1_HousingControlArea|
||居住環境向上用途誘導地区|〇|lod1_ResidentialEnvironmentImprovementDistrict|
||特定用途誘導地区|〇|lod1_SpecialUseAttractionDistrict|
||防火地域又は準防火地域|〇|lod1_FirePreventionDistrict|
||特定防災街区整備地区|〇|lod1_SpecifiedDisasterPreventionBlockImprovementZone|
||景観地区|〇|lod1_LandscapeZone|
||風致地区|〇|lod1_ScenicDistrict|
||駐車場整備地区|〇|lod1_ParkingPlaceDevelopmentZone|
||臨港地区|〇|lod1_PortZone|
||歴史的風土特別保存地区|〇|lod1_SpecialZoneForPreservationOfHistoricalLandscape|
||第一種歴史的風土保存地区又は第二種歴史的風土保存地区|〇|lod1_ZoneForPreservationOfHistoricalLandscape|
||緑地保全地域|〇|lod1_GreenSpaceConservationDistrict|
||特別緑地保全地域|〇|lod1_SpecialGreenSpaceConservationDistrict|
||緑化地域|〇|lod1_TreePlantingDistrict|
||流通業務地区|〇|lod1_DistributionBusinessZone|
||生産緑地地区|〇|lod1_ProductiveGreenZone|
||伝統的建造物群保存地区|〇|lod1_ConservationZoneForClustersOfTraditionalStructures|
||航空機騒音障害防止地区又は航空機騒音障害防止特別地区|〇|lod1_AircraftNoiseControlZone|

※ 変換されるファイル ジオデータベースの詳細な定義は、[3D 都市モデルデータ変換ツール v2.0 for ArcGIS 操作マニュアルの付属資料](https://github.com/EsriJapan/3D-CityModel-ConversionTools-for-ArcGIS-v2/blob/main/Doc/%EF%BC%93D%20%E9%83%BD%E5%B8%82%E3%83%A2%E3%83%87%E3%83%AB%E3%83%87%E3%83%BC%E3%82%BF%E5%A4%89%E6%8F%9B%E3%83%84%E3%83%BC%E3%83%AB%20v2.0%20for%20ArcGIS%20%E6%93%8D%E4%BD%9C%E3%83%9E%E3%83%8B%E3%83%A5%E3%82%A2%E3%83%AB%202.0.0%20%E7%89%88%EF%BC%88%E8%A3%BD%E5%93%81%E4%BB%95%E6%A7%98%E6%9B%B8%20%E7%AC%AC%202.3%20%E7%89%88%E5%AF%BE%E5%BF%9C%EF%BC%89_%E4%BB%98%E5%B1%9E%E8%B3%87%E6%96%99.xlsx)をご参照ください。

## 動作環境
本ツールを実行するには、バージョン 3.1 以上の ArcGIS Pro と ArcGIS Data Interoperability エクステンション をインストールし（ArcGIS Pro とArcGIS Data Interoperability のインストーラーは、それぞれ別々に提供されております。My Esri からそれぞれのインストーラーを入手いただき、インストールして頂く必要があります）、ライセンスを有効化している必要があります。  
詳細な動作環境、およびData Interoperability エクステンション のインストール方法は、以下をご参照ください。
* [ArcGIS Pro の動作環境](https://www.esrij.com/products/arcgis-pro/spec/)
* [Data Interoperability エクステンションのインストール](https://pro.arcgis.com/ja/pro-app/latest/help/data/data-interoperability/install-the-data-interoperability-extension.htm)  

### 利用方法
本ツールを使って変換するまでには、大まかに次のステップが必要です。操作方法の詳細は[3D 都市モデルデータ変換ツール v2.0 for ArcGIS 操作マニュアル](https://github.com/EsriJapan/3D-CityModel-ConversionTools-for-ArcGIS-v2/blob/main/Doc/%EF%BC%93D%20%E9%83%BD%E5%B8%82%E3%83%A2%E3%83%87%E3%83%AB%E3%83%87%E3%83%BC%E3%82%BF%E5%A4%89%E6%8F%9B%E3%83%84%E3%83%BC%E3%83%AB%20v2.0%20for%20ArcGIS%20%E6%93%8D%E4%BD%9C%E3%83%9E%E3%83%8B%E3%83%A5%E3%82%A2%E3%83%AB%202.0.0%20%E7%89%88%EF%BC%88%E8%A3%BD%E5%93%81%E4%BB%95%E6%A7%98%E6%9B%B8%20%E7%AC%AC%202.3%20%E7%89%88%E5%AF%BE%E5%BF%9C%EF%BC%89.pdf) をご参照ください。

* [3D 都市モデルデータ変換ツール v2.0 for ArcGIS をダウンロード](https://github.com/EsriJapan/3D-CityModel-ConversionTools-for-ArcGIS-v2/releases/download/v2.0.0/3D_CityModel_ConversionTools_v2.zip)します。
* ダウンロードした ZIP ファイルを、任意の場所に解凍します。このとき、ツールのフルパスにマルチバイト文字が含まれないようにしてください。
* ArcGIS Pro を起動し、フォルダー接続の追加 で、解凍したフォルダーを指定します。
* G空間情報センターから、必要な 3D 都市モデル（標準製品仕様書 第2.3版に基づいて作成された CityGML）のデータをダウンロードし、解凍しておきます。このとき、データのフルパスにマルチバイト文字が含まれないようにしてください。
* 操作マニュアルの「2.4 3D 都市モデルデータ変換ツールの実行方法」を参照しながら、それぞれの地物を変換します。
* 必要に応じて、汎用属性セットをフィールドに展開するスクリプトツールを実行します。

### 免責事項
* 本ツールに含まれるカスタムツールは、サンプルとして提供しているものであり、動作に関する保証、および製品ライフサイクルに従った Esri 製品サポート サービスは提供しておりません。
* 本ツールに含まれるツールによって生じた損失及び損害等について、一切の責任を負いかねますのでご了承ください。
* 弊社で提供している Esri 製品サポートサービスでは、本ツールに関しての Ｑ＆Ａ サポートの受付を行っておりませんので、予めご了承の上、ご利用ください。詳細は[
ESRIジャパン GitHub アカウントにおけるオープンソースへの貢献について](https://github.com/EsriJapan/contributing)をご参照ください。

## ライセンス
Copyright 2023 Esri Japan Corporation.

Apache License Version 2.0（「本ライセンス」）に基づいてライセンスされます。あなたがこのファイルを使用するためには、本ライセンスに従わなければなりません。
本ライセンスのコピーは下記の場所から入手できます。

> http://www.apache.org/licenses/LICENSE-2.0

適用される法律または書面での同意によって命じられない限り、本ライセンスに基づいて頒布されるソフトウェアは、明示黙示を問わず、いかなる保証も条件もなしに「現状のまま」頒布されます。本ライセンスでの権利と制限を規定した文言については、本ライセンスを参照してください。

ライセンスのコピーは本リポジトリの[ライセンス ファイル](./LICENSE)で利用可能です。
