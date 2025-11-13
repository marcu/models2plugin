"""Tests for the replace_qml_paths_in_model_content function."""

from models2plugin.qml_parser import replace_qml_paths_in_model_content


def test_replace_qml_paths_single():
    """Test replacing a single QML path in model content."""
    model_content = '''<?xml version="1.0" encoding="UTF-8"?>
<Model>
  <Option name="STYLE" type="List">
    <Option type="Map">
      <Option value="2" name="source" type="int"/>
      <Option value="C:\\Users\\NoPiT\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\processing\\models\\Parcelles dans la zone.qml" name="static_value" type="QString"/>
    </Option>
  </Option>
</Model>'''

    new_models_dir = r"C:\Users\Autreutilisateur\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\models"
    modified_content = replace_qml_paths_in_model_content(model_content, new_models_dir)
    
    expected_path = r"C:\Users\Autreutilisateur\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\models\Parcelles dans la zone.qml"
    assert expected_path in modified_content
    assert r"C:\Users\NoPiT\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\models\Parcelles dans la zone.qml" not in modified_content


def test_replace_qml_paths_multiple():
    """Test replacing multiple QML paths in model content."""
    model_content = '''<?xml version="1.0" encoding="UTF-8"?>
<Model>
  <Option name="STYLE" type="List">
    <Option type="Map">
      <Option value="2" name="source" type="int"/>
      <Option value="C:\\path\\to\\style1.qml" name="static_value" type="QString"/>
    </Option>
    <Option type="Map">
      <Option value="2" name="source" type="int"/>
      <Option value="C:\\path\\to\\style2.qml" name="static_value" type="QString"/>
    </Option>
  </Option>
</Model>'''

    new_models_dir = r"C:\Users\Autreutilisateur\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\models"
    modified_content = replace_qml_paths_in_model_content(model_content, new_models_dir)
    
    expected_path1 = r"C:\Users\Autreutilisateur\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\models\style1.qml"
    expected_path2 = r"C:\Users\Autreutilisateur\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\models\style2.qml"
    
    assert expected_path1 in modified_content
    assert expected_path2 in modified_content
    assert r"C:\path\to\style1.qml" not in modified_content
    assert r"C:\path\to\style2.qml" not in modified_content


def test_replace_qml_paths_with_type_list_first():
    """Test replacing QML paths when type="List" comes before name="STYLE"."""
    model_content = '''<?xml version="1.0" encoding="UTF-8"?>
<Model>
  <Option type="List" name="STYLE">
    <Option type="Map">
      <Option value="2" name="source" type="int"/>
      <Option value="C:\\path\\to\\style.qml" name="static_value" type="QString"/>
    </Option>
  </Option>
</Model>'''

    new_models_dir = r"C:\Users\Autreutilisateur\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\models"
    modified_content = replace_qml_paths_in_model_content(model_content, new_models_dir)
    
    expected_path = r"C:\Users\Autreutilisateur\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\models\style.qml"
    assert expected_path in modified_content
    assert r"C:\path\to\style.qml" not in modified_content

def test_replace_qml_paths_real_life():
    """Test with my file"""
    model_content = r'''<!DOCTYPE model>
<Option type="Map">
  <Option type="Map" name="children">
    <Option type="Map" name="native:buffer_1">
      <Option value="true" type="bool" name="active"/>
      <Option name="alg_config"/>
      <Option value="native:buffer" type="QString" name="alg_id"/>
      <Option value="" type="QString" name="color"/>
      <Option type="Map" name="comment">
        <Option value="" type="QString" name="color"/>
        <Option value="" type="QString" name="component_description"/>
        <Option value="60" type="double" name="component_height"/>
        <Option value="931.6702500000001" type="double" name="component_pos_x"/>
        <Option value="433.543375" type="double" name="component_pos_y"/>
        <Option value="100" type="double" name="component_width"/>
        <Option value="true" type="bool" name="outputs_collapsed"/>
        <Option value="true" type="bool" name="parameters_collapsed"/>
      </Option>
      <Option value="Tampon" type="QString" name="component_description"/>
      <Option value="30" type="double" name="component_height"/>
      <Option value="718.001036310108" type="double" name="component_pos_x"/>
      <Option value="468.1311930814524" type="double" name="component_pos_y"/>
      <Option value="200" type="double" name="component_width"/>
      <Option name="dependencies"/>
      <Option value="native:buffer_1" type="QString" name="id"/>
      <Option name="outputs"/>
      <Option value="true" type="bool" name="outputs_collapsed"/>
      <Option value="true" type="bool" name="parameters_collapsed"/>
      <Option type="Map" name="params">
        <Option type="List" name="DISSOLVE">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option value="true" type="bool" name="static_value"/>
          </Option>
        </Option>
        <Option type="List" name="DISTANCE">
          <Option type="Map">
            <Option value="nombre_de_mtres_du_tampon" type="QString" name="parameter_name"/>
            <Option value="0" type="int" name="source"/>
          </Option>
        </Option>
        <Option type="List" name="END_CAP_STYLE">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option value="0" type="int" name="static_value"/>
          </Option>
        </Option>
        <Option type="List" name="INPUT">
          <Option type="Map">
            <Option value="native:extractbyattribute_1" type="QString" name="child_id"/>
            <Option value="OUTPUT" type="QString" name="output_name"/>
            <Option value="1" type="int" name="source"/>
          </Option>
        </Option>
        <Option type="List" name="JOIN_STYLE">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option value="0" type="int" name="static_value"/>
          </Option>
        </Option>
        <Option type="List" name="MITER_LIMIT">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option value="1" type="double" name="static_value"/>
          </Option>
        </Option>
        <Option type="List" name="SEGMENTS">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option value="5" type="int" name="static_value"/>
          </Option>
        </Option>
        <Option type="List" name="SEPARATE_DISJOINT">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option value="false" type="bool" name="static_value"/>
          </Option>
        </Option>
      </Option>
    </Option>
    <Option type="Map" name="native:exporttospreadsheet_1">
      <Option value="true" type="bool" name="active"/>
      <Option name="alg_config"/>
      <Option value="native:exporttospreadsheet" type="QString" name="alg_id"/>
      <Option value="" type="QString" name="color"/>
      <Option type="Map" name="comment">
        <Option value="" type="QString" name="color"/>
        <Option value="" type="QString" name="component_description"/>
        <Option value="60" type="double" name="component_height"/>
        <Option value="1193.9399787605084" type="double" name="component_pos_x"/>
        <Option value="643.5985309154746" type="double" name="component_pos_y"/>
        <Option value="100" type="double" name="component_width"/>
        <Option value="true" type="bool" name="outputs_collapsed"/>
        <Option value="true" type="bool" name="parameters_collapsed"/>
      </Option>
      <Option value="Exporter vers un tableur" type="QString" name="component_description"/>
      <Option value="35.58573262687809" type="double" name="component_height"/>
      <Option value="970.2006150962761" type="double" name="component_pos_x"/>
      <Option value="703.9592956393897" type="double" name="component_pos_y"/>
      <Option value="200" type="double" name="component_width"/>
      <Option name="dependencies"/>
      <Option value="native:exporttospreadsheet_1" type="QString" name="id"/>
      <Option type="Map" name="outputs">
        <Option type="Map" name="Export parcelles dans zone">
          <Option value="native:exporttospreadsheet_1" type="QString" name="child_id"/>
          <Option value="" type="QString" name="color"/>
          <Option type="Map" name="comment">
            <Option value="" type="QString" name="color"/>
            <Option value="" type="QString" name="component_description"/>
            <Option value="60" type="double" name="component_height"/>
            <Option value="0" type="double" name="component_pos_x"/>
            <Option value="0" type="double" name="component_pos_y"/>
            <Option value="100" type="double" name="component_width"/>
            <Option value="true" type="bool" name="outputs_collapsed"/>
            <Option value="true" type="bool" name="parameters_collapsed"/>
          </Option>
          <Option value="Export parcelles dans zone" type="QString" name="component_description"/>
          <Option value="30" type="double" name="component_height"/>
          <Option value="1109.1401204034496" type="double" name="component_pos_x"/>
          <Option value="762.7675358794166" type="double" name="component_pos_y"/>
          <Option value="200" type="double" name="component_width"/>
          <Option type="invalid" name="default_value"/>
          <Option value="false" type="bool" name="mandatory"/>
          <Option value="Export parcelles dans zone" type="QString" name="name"/>
          <Option value="OUTPUT" type="QString" name="output_name"/>
          <Option value="true" type="bool" name="outputs_collapsed"/>
          <Option value="true" type="bool" name="parameters_collapsed"/>
        </Option>
      </Option>
      <Option value="true" type="bool" name="outputs_collapsed"/>
      <Option value="true" type="bool" name="parameters_collapsed"/>
      <Option type="Map" name="params">
        <Option type="List" name="FORMATTED_VALUES">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option value="false" type="bool" name="static_value"/>
          </Option>
        </Option>
        <Option type="List" name="LAYERS">
          <Option type="Map">
            <Option value="native:intersection_1" type="QString" name="child_id"/>
            <Option value="OUTPUT" type="QString" name="output_name"/>
            <Option value="1" type="int" name="source"/>
          </Option>
        </Option>
        <Option type="List" name="OVERWRITE">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option value="true" type="bool" name="static_value"/>
          </Option>
        </Option>
        <Option type="List" name="USE_ALIAS">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option value="false" type="bool" name="static_value"/>
          </Option>
        </Option>
      </Option>
    </Option>
    <Option type="Map" name="native:extractbyattribute_1">
      <Option value="true" type="bool" name="active"/>
      <Option name="alg_config"/>
      <Option value="native:extractbyattribute" type="QString" name="alg_id"/>
      <Option value="" type="QString" name="color"/>
      <Option type="Map" name="comment">
        <Option value="" type="QString" name="color"/>
        <Option value="" type="QString" name="component_description"/>
        <Option value="60" type="double" name="component_height"/>
        <Option value="1277.9026250000002" type="double" name="component_pos_x"/>
        <Option value="725" type="double" name="component_pos_y"/>
        <Option value="100" type="double" name="component_width"/>
        <Option value="true" type="bool" name="outputs_collapsed"/>
        <Option value="true" type="bool" name="parameters_collapsed"/>
      </Option>
      <Option value="Extraire par attribut - Filtre EDE" type="QString" name="component_description"/>
      <Option value="30" type="double" name="component_height"/>
      <Option value="548.602568950264" type="double" name="component_pos_x"/>
      <Option value="372.30524098346933" type="double" name="component_pos_y"/>
      <Option value="200" type="double" name="component_width"/>
      <Option name="dependencies"/>
      <Option value="native:extractbyattribute_1" type="QString" name="id"/>
      <Option type="Map" name="outputs">
        <Option type="Map" name="Parcelles ede enquête">
          <Option value="native:extractbyattribute_1" type="QString" name="child_id"/>
          <Option value="" type="QString" name="color"/>
          <Option type="Map" name="comment">
            <Option value="" type="QString" name="color"/>
            <Option value="" type="QString" name="component_description"/>
            <Option value="60" type="double" name="component_height"/>
            <Option value="0" type="double" name="component_pos_x"/>
            <Option value="0" type="double" name="component_pos_y"/>
            <Option value="100" type="double" name="component_width"/>
            <Option value="true" type="bool" name="outputs_collapsed"/>
            <Option value="true" type="bool" name="parameters_collapsed"/>
          </Option>
          <Option value="Parcelles ede enquête" type="QString" name="component_description"/>
          <Option value="30" type="double" name="component_height"/>
          <Option value="836.8010477183516" type="double" name="component_pos_x"/>
          <Option value="352.50794344946013" type="double" name="component_pos_y"/>
          <Option value="200" type="double" name="component_width"/>
          <Option type="invalid" name="default_value"/>
          <Option value="false" type="bool" name="mandatory"/>
          <Option value="Parcelles ede enquête" type="QString" name="name"/>
          <Option value="OUTPUT" type="QString" name="output_name"/>
          <Option value="true" type="bool" name="outputs_collapsed"/>
          <Option value="true" type="bool" name="parameters_collapsed"/>
        </Option>
      </Option>
      <Option value="true" type="bool" name="outputs_collapsed"/>
      <Option value="true" type="bool" name="parameters_collapsed"/>
      <Option type="Map" name="params">
        <Option type="List" name="FIELD">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option value="ede_siret" type="QString" name="static_value"/>
          </Option>
        </Option>
        <Option type="List" name="INPUT">
          <Option type="Map">
            <Option value="parcellaire" type="QString" name="parameter_name"/>
            <Option value="0" type="int" name="source"/>
          </Option>
        </Option>
        <Option type="List" name="OPERATOR">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option value="0" type="int" name="static_value"/>
          </Option>
        </Option>
        <Option type="List" name="VALUE">
          <Option type="Map">
            <Option value="ede_sinon_siret" type="QString" name="parameter_name"/>
            <Option value="0" type="int" name="source"/>
          </Option>
        </Option>
      </Option>
    </Option>
    <Option type="Map" name="native:extractbyattribute_2">
      <Option value="true" type="bool" name="active"/>
      <Option name="alg_config"/>
      <Option value="native:extractbyattribute" type="QString" name="alg_id"/>
      <Option value="" type="QString" name="color"/>
      <Option type="Map" name="comment">
        <Option value="" type="QString" name="color"/>
        <Option value="" type="QString" name="component_description"/>
        <Option value="60" type="double" name="component_height"/>
        <Option value="1328.510035083415" type="double" name="component_pos_x"/>
        <Option value="737.3195634200198" type="double" name="component_pos_y"/>
        <Option value="100" type="double" name="component_width"/>
        <Option value="true" type="bool" name="outputs_collapsed"/>
        <Option value="true" type="bool" name="parameters_collapsed"/>
      </Option>
      <Option value="Extraire par attribut - Filtre autres parcelles" type="QString" name="component_description"/>
      <Option value="41.908215219319054" type="double" name="component_height"/>
      <Option value="464.27395953489275" type="double" name="component_pos_x"/>
      <Option value="519.3907857914096" type="double" name="component_pos_y"/>
      <Option value="200" type="double" name="component_width"/>
      <Option name="dependencies"/>
      <Option value="native:extractbyattribute_2" type="QString" name="id"/>
      <Option name="outputs"/>
      <Option value="true" type="bool" name="outputs_collapsed"/>
      <Option value="true" type="bool" name="parameters_collapsed"/>
      <Option type="Map" name="params">
        <Option type="List" name="FIELD">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option value="ede_siret" type="QString" name="static_value"/>
          </Option>
        </Option>
        <Option type="List" name="INPUT">
          <Option type="Map">
            <Option value="parcellaire" type="QString" name="parameter_name"/>
            <Option value="0" type="int" name="source"/>
          </Option>
        </Option>
        <Option type="List" name="OPERATOR">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option value="1" type="int" name="static_value"/>
          </Option>
        </Option>
        <Option type="List" name="VALUE">
          <Option type="Map">
            <Option value="ede_sinon_siret" type="QString" name="parameter_name"/>
            <Option value="0" type="int" name="source"/>
          </Option>
        </Option>
      </Option>
    </Option>
    <Option type="Map" name="native:intersection_1">
      <Option value="true" type="bool" name="active"/>
      <Option name="alg_config"/>
      <Option value="native:intersection" type="QString" name="alg_id"/>
      <Option value="" type="QString" name="color"/>
      <Option type="Map" name="comment">
        <Option value="" type="QString" name="color"/>
        <Option value="" type="QString" name="component_description"/>
        <Option value="60" type="double" name="component_height"/>
        <Option value="1057.9026250000002" type="double" name="component_pos_x"/>
        <Option value="625" type="double" name="component_pos_y"/>
        <Option value="100" type="double" name="component_width"/>
        <Option value="true" type="bool" name="outputs_collapsed"/>
        <Option value="true" type="bool" name="parameters_collapsed"/>
      </Option>
      <Option value="Intersection" type="QString" name="component_description"/>
      <Option value="30" type="double" name="component_height"/>
      <Option value="773.9399787605083" type="double" name="component_pos_x"/>
      <Option value="588.5985309154746" type="double" name="component_pos_y"/>
      <Option value="200" type="double" name="component_width"/>
      <Option name="dependencies"/>
      <Option value="native:intersection_1" type="QString" name="id"/>
      <Option type="Map" name="outputs">
        <Option type="Map" name="Parcelles dans la zone">
          <Option value="native:intersection_1" type="QString" name="child_id"/>
          <Option value="" type="QString" name="color"/>
          <Option type="Map" name="comment">
            <Option value="" type="QString" name="color"/>
            <Option value="" type="QString" name="component_description"/>
            <Option value="60" type="double" name="component_height"/>
            <Option value="0" type="double" name="component_pos_x"/>
            <Option value="0" type="double" name="component_pos_y"/>
            <Option value="100" type="double" name="component_width"/>
            <Option value="true" type="bool" name="outputs_collapsed"/>
            <Option value="true" type="bool" name="parameters_collapsed"/>
          </Option>
          <Option value="Parcelles dans la zone" type="QString" name="component_description"/>
          <Option value="51.50486173016657" type="double" name="component_height"/>
          <Option value="949.8919960284155" type="double" name="component_pos_x"/>
          <Option value="534.5332814990929" type="double" name="component_pos_y"/>
          <Option value="200" type="double" name="component_width"/>
          <Option type="Map" name="default_value">
            <Option value="QgsProcessingOutputLayerDefinition" type="QString" name="class"/>
            <Option type="Map" name="create_options">
              <Option value="windows-1252" type="QString" name="fileEncoding"/>
            </Option>
            <Option type="Map" name="sink">
              <Option value="true" type="bool" name="active"/>
              <Option value="1" type="int" name="type"/>
              <Option value="TEMPORARY_OUTPUT" type="QString" name="val"/>
            </Option>
          </Option>
          <Option value="true" type="bool" name="mandatory"/>
          <Option value="Parcelles dans la zone" type="QString" name="name"/>
          <Option value="OUTPUT" type="QString" name="output_name"/>
          <Option value="true" type="bool" name="outputs_collapsed"/>
          <Option value="true" type="bool" name="parameters_collapsed"/>
        </Option>
      </Option>
      <Option value="true" type="bool" name="outputs_collapsed"/>
      <Option value="true" type="bool" name="parameters_collapsed"/>
      <Option type="Map" name="params">
        <Option type="List" name="GRID_SIZE">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option type="invalid" name="static_value"/>
          </Option>
        </Option>
        <Option type="List" name="INPUT">
          <Option type="Map">
            <Option value="native:extractbyattribute_2" type="QString" name="child_id"/>
            <Option value="OUTPUT" type="QString" name="output_name"/>
            <Option value="1" type="int" name="source"/>
          </Option>
        </Option>
        <Option type="List" name="INPUT_FIELDS">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option type="StringList" name="static_value">
              <Option value="" type="QString"/>
            </Option>
          </Option>
        </Option>
        <Option type="List" name="OVERLAY">
          <Option type="Map">
            <Option value="native:buffer_1" type="QString" name="child_id"/>
            <Option value="OUTPUT" type="QString" name="output_name"/>
            <Option value="1" type="int" name="source"/>
          </Option>
        </Option>
        <Option type="List" name="OVERLAY_FIELDS">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option type="StringList" name="static_value">
              <Option value="" type="QString"/>
            </Option>
          </Option>
        </Option>
        <Option type="List" name="OVERLAY_FIELDS_PREFIX">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option type="invalid" name="static_value"/>
          </Option>
        </Option>
      </Option>
    </Option>
    <Option type="Map" name="native:setlayerstyle_1">
      <Option value="true" type="bool" name="active"/>
      <Option name="alg_config"/>
      <Option value="native:setlayerstyle" type="QString" name="alg_id"/>
      <Option value="" type="QString" name="color"/>
      <Option type="Map" name="comment">
        <Option value="255,140,141,255,hsv:0.99833333333333329,0.45185015640497445,1,1" type="QString" name="color"/>
        <Option value="MODIFIER ICI style &quot;Parcelle ede enquête&quot;" type="QString" name="component_description"/>
        <Option value="60" type="double" name="component_height"/>
        <Option value="1095.435035022933" type="double" name="component_pos_x"/>
        <Option value="387.9860290104993" type="double" name="component_pos_y"/>
        <Option value="100" type="double" name="component_width"/>
        <Option value="true" type="bool" name="outputs_collapsed"/>
        <Option value="true" type="bool" name="parameters_collapsed"/>
      </Option>
      <Option value="Appliquer le style" type="QString" name="component_description"/>
      <Option value="30" type="double" name="component_height"/>
      <Option value="908.2479835229807" type="double" name="component_pos_x"/>
      <Option value="408.5087827124373" type="double" name="component_pos_y"/>
      <Option value="200" type="double" name="component_width"/>
      <Option name="dependencies"/>
      <Option value="native:setlayerstyle_1" type="QString" name="id"/>
      <Option name="outputs"/>
      <Option value="true" type="bool" name="outputs_collapsed"/>
      <Option value="true" type="bool" name="parameters_collapsed"/>
      <Option type="Map" name="params">
        <Option type="List" name="INPUT">
          <Option type="Map">
            <Option value="native:extractbyattribute_1" type="QString" name="child_id"/>
            <Option value="FAIL_OUTPUT" type="QString" name="output_name"/>
            <Option value="1" type="int" name="source"/>
          </Option>
        </Option>
        <Option type="List" name="STYLE">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option value="C:\Users\NoPiT\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\models\Parcelle ede enquête.qml" type="QString" name="static_value"/>
          </Option>
        </Option>
      </Option>
    </Option>
    <Option type="Map" name="native:setlayerstyle_2">
      <Option value="true" type="bool" name="active"/>
      <Option name="alg_config"/>
      <Option value="native:setlayerstyle" type="QString" name="alg_id"/>
      <Option value="" type="QString" name="color"/>
      <Option type="Map" name="comment">
        <Option value="255,133,134,255,hsv:0.99833333333333329,0.4802319371328298,1,1" type="QString" name="color"/>
        <Option value="MODIFIER ICI style &quot;Parcelle dans la zone&quot;" type="QString" name="component_description"/>
        <Option value="60" type="double" name="component_height"/>
        <Option value="1194.6488156329851" type="double" name="component_pos_x"/>
        <Option value="461.31795380923353" type="double" name="component_pos_y"/>
        <Option value="100" type="double" name="component_width"/>
        <Option value="true" type="bool" name="outputs_collapsed"/>
        <Option value="true" type="bool" name="parameters_collapsed"/>
      </Option>
      <Option value="Appliquer le style" type="QString" name="component_description"/>
      <Option value="37.16828724338882" type="double" name="component_height"/>
      <Option value="1021.7458648766376" type="double" name="component_pos_x"/>
      <Option value="473.0233679029372" type="double" name="component_pos_y"/>
      <Option value="200" type="double" name="component_width"/>
      <Option name="dependencies"/>
      <Option value="native:setlayerstyle_2" type="QString" name="id"/>
      <Option name="outputs"/>
      <Option value="true" type="bool" name="outputs_collapsed"/>
      <Option value="true" type="bool" name="parameters_collapsed"/>
      <Option type="Map" name="params">
        <Option type="List" name="INPUT">
          <Option type="Map">
            <Option value="native:intersection_1" type="QString" name="child_id"/>
            <Option value="OUTPUT" type="QString" name="output_name"/>
            <Option value="1" type="int" name="source"/>
          </Option>
        </Option>
        <Option type="List" name="STYLE">
          <Option type="Map">
            <Option value="2" type="int" name="source"/>
            <Option value="C:\Users\NoPiT\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\models\Parcelles dans la zone.qml" type="QString" name="static_value"/>
          </Option>
        </Option>
      </Option>
    </Option>
  </Option>
  <Option type="Map" name="designerParameterValues">
    <Option value="TEMPORARY_OUTPUT" type="QString" name="export_parcelles_dans_zone"/>
    <Option value="100" type="double" name="nombre_de_mtres_du_tampon"/>
    <Option value="v_parcelle_mat_a6c1c269_6ab7_48c4_a57c_46ef015ec7b4" type="QString" name="parcellaire"/>
    <Option type="QgsProcessingOutputLayerDefinition" name="parcelles_dans_la_zone">
      <Option type="Map">
        <Option type="Map" name="create_options">
          <Option value="windows-1252" type="QString" name="fileEncoding"/>
        </Option>
        <Option type="Map" name="sink">
          <Option value="true" type="bool" name="active"/>
          <Option value="1" type="int" name="type"/>
          <Option value="TEMPORARY_OUTPUT" type="QString" name="val"/>
        </Option>
      </Option>
    </Option>
    <Option type="QgsProcessingOutputLayerDefinition" name="parcelles_ede_enqute">
      <Option type="Map">
        <Option type="Map" name="create_options">
          <Option value="windows-1252" type="QString" name="fileEncoding"/>
        </Option>
        <Option type="Map" name="sink">
          <Option value="true" type="bool" name="active"/>
          <Option value="1" type="int" name="type"/>
          <Option value="TEMPORARY_OUTPUT" type="QString" name="val"/>
        </Option>
      </Option>
    </Option>
    <Option value="true" type="bool" name="uniquement_les_parcelles_pturage"/>
  </Option>
  <Option name="groupBoxes"/>
  <Option name="help"/>
  <Option value="Version2" type="QString" name="internal_version"/>
  <Option name="modelVariables"/>
  <Option value="" type="QString" name="model_group"/>
  <Option value="Zonage intersection parcellaire (savoie version)" type="QString" name="model_name"/>
  <Option value="Zonage intersection parcellaire" type="QString" name="outputGroup"/>
  <Option type="StringList" name="outputOrder">
    <Option value="native:exporttospreadsheet_1:OUTPUT" type="QString"/>
    <Option value="native:intersection_1:OUTPUT" type="QString"/>
    <Option value="native:extractbyattribute_1:OUTPUT" type="QString"/>
  </Option>
  <Option type="Map" name="parameterDefinitions">
    <Option type="Map" name="ede_sinon_siret">
      <Option value="63144191" type="QString" name="default"/>
      <Option type="invalid" name="defaultGui"/>
      <Option value="EDE sinon Siret" type="QString" name="description"/>
      <Option value="0" type="int" name="flags"/>
      <Option value="" type="QString" name="help"/>
      <Option name="metadata"/>
      <Option value="false" type="bool" name="multiline"/>
      <Option value="ede_sinon_siret" type="QString" name="name"/>
      <Option value="string" type="QString" name="parameter_type"/>
    </Option>
    <Option type="Map" name="export_parcelles_dans_zone">
      <Option value="true" type="bool" name="create_by_default"/>
      <Option type="invalid" name="default"/>
      <Option type="invalid" name="defaultGui"/>
      <Option value="Export parcelles dans zone" type="QString" name="description"/>
      <Option value="Microsoft Excel (*.xlsx);;Open Document Spreadsheet (*.ods)" type="QString" name="file_filter"/>
      <Option value="0" type="int" name="flags"/>
      <Option value="" type="QString" name="help"/>
      <Option type="Map" name="metadata">
        <Option value="native:exporttospreadsheet_1" type="QString" name="_modelChildId"/>
        <Option value="Export parcelles dans zone" type="QString" name="_modelChildOutputName"/>
        <Option value="native" type="QString" name="_modelChildProvider"/>
        <Option type="Map" name="widget_wrapper">
          <Option value="true" type="bool" name="dontconfirmoverwrite"/>
        </Option>
      </Option>
      <Option value="export_parcelles_dans_zone" type="QString" name="name"/>
      <Option value="fileDestination" type="QString" name="parameter_type"/>
      <Option value="true" type="bool" name="supports_non_file_outputs"/>
    </Option>
    <Option type="Map" name="nombre_de_mtres_du_tampon">
      <Option value="1" type="int" name="data_type"/>
      <Option value="10" type="double" name="default"/>
      <Option type="invalid" name="defaultGui"/>
      <Option value="Nombre de mètres du tampon" type="QString" name="description"/>
      <Option value="0" type="int" name="flags"/>
      <Option value="" type="QString" name="help"/>
      <Option value="1e+06" type="double" name="max"/>
      <Option name="metadata"/>
      <Option value="0" type="double" name="min"/>
      <Option value="nombre_de_mtres_du_tampon" type="QString" name="name"/>
      <Option value="number" type="QString" name="parameter_type"/>
    </Option>
    <Option type="Map" name="parcellaire">
      <Option type="List" name="data_types">
        <Option value="2" type="int"/>
      </Option>
      <Option type="invalid" name="default"/>
      <Option type="invalid" name="defaultGui"/>
      <Option value="Parcellaire" type="QString" name="description"/>
      <Option value="0" type="int" name="flags"/>
      <Option value="" type="QString" name="help"/>
      <Option name="metadata"/>
      <Option value="parcellaire" type="QString" name="name"/>
      <Option value="vector" type="QString" name="parameter_type"/>
    </Option>
    <Option type="Map" name="parcelles_dans_la_zone">
      <Option value="true" type="bool" name="create_by_default"/>
      <Option value="-1" type="int" name="data_type"/>
      <Option type="QgsProcessingOutputLayerDefinition" name="default">
        <Option type="Map">
          <Option type="Map" name="create_options">
            <Option value="windows-1252" type="QString" name="fileEncoding"/>
          </Option>
          <Option type="Map" name="sink">
            <Option value="true" type="bool" name="active"/>
            <Option value="1" type="int" name="type"/>
            <Option value="TEMPORARY_OUTPUT" type="QString" name="val"/>
          </Option>
        </Option>
      </Option>
      <Option type="invalid" name="defaultGui"/>
      <Option value="Parcelles dans la zone" type="QString" name="description"/>
      <Option value="0" type="int" name="flags"/>
      <Option value="" type="QString" name="help"/>
      <Option type="Map" name="metadata">
        <Option value="native:intersection_1" type="QString" name="_modelChildId"/>
        <Option value="Parcelles dans la zone" type="QString" name="_modelChildOutputName"/>
        <Option value="native" type="QString" name="_modelChildProvider"/>
      </Option>
      <Option value="parcelles_dans_la_zone" type="QString" name="name"/>
      <Option value="sink" type="QString" name="parameter_type"/>
      <Option value="false" type="bool" name="supports_append"/>
      <Option value="true" type="bool" name="supports_non_file_outputs"/>
    </Option>
    <Option type="Map" name="parcelles_ede_enqute">
      <Option value="true" type="bool" name="create_by_default"/>
      <Option value="-1" type="int" name="data_type"/>
      <Option type="invalid" name="default"/>
      <Option type="invalid" name="defaultGui"/>
      <Option value="Parcelles ede enquête" type="QString" name="description"/>
      <Option value="0" type="int" name="flags"/>
      <Option value="" type="QString" name="help"/>
      <Option type="Map" name="metadata">
        <Option value="native:extractbyattribute_1" type="QString" name="_modelChildId"/>
        <Option value="Parcelles ede enquête" type="QString" name="_modelChildOutputName"/>
        <Option value="native" type="QString" name="_modelChildProvider"/>
      </Option>
      <Option value="parcelles_ede_enqute" type="QString" name="name"/>
      <Option value="sink" type="QString" name="parameter_type"/>
      <Option value="false" type="bool" name="supports_append"/>
      <Option value="true" type="bool" name="supports_non_file_outputs"/>
    </Option>
  </Option>
  <Option name="parameterOrder"/>
  <Option type="Map" name="parameters">
    <Option type="Map" name="ede_sinon_siret">
      <Option value="" type="QString" name="color"/>
      <Option type="Map" name="comment">
        <Option value="" type="QString" name="color"/>
        <Option value="" type="QString" name="component_description"/>
        <Option value="60" type="double" name="component_height"/>
        <Option value="683.6740625" type="double" name="component_pos_x"/>
        <Option value="15" type="double" name="component_pos_y"/>
        <Option value="100" type="double" name="component_width"/>
        <Option value="true" type="bool" name="outputs_collapsed"/>
        <Option value="true" type="bool" name="parameters_collapsed"/>
      </Option>
      <Option value="ede_sinon_siret" type="QString" name="component_description"/>
      <Option value="41" type="double" name="component_height"/>
      <Option value="160.18421549020198" type="double" name="component_pos_x"/>
      <Option value="337.2922303522047" type="double" name="component_pos_y"/>
      <Option value="200" type="double" name="component_width"/>
      <Option value="ede_sinon_siret" type="QString" name="name"/>
      <Option value="true" type="bool" name="outputs_collapsed"/>
      <Option value="true" type="bool" name="parameters_collapsed"/>
    </Option>
    <Option type="Map" name="nombre_de_mtres_du_tampon">
      <Option value="" type="QString" name="color"/>
      <Option type="Map" name="comment">
        <Option value="" type="QString" name="color"/>
        <Option value="" type="QString" name="component_description"/>
        <Option value="60" type="double" name="component_height"/>
        <Option value="640.7906875" type="double" name="component_pos_x"/>
        <Option value="15" type="double" name="component_pos_y"/>
        <Option value="100" type="double" name="component_width"/>
        <Option value="true" type="bool" name="outputs_collapsed"/>
        <Option value="true" type="bool" name="parameters_collapsed"/>
      </Option>
      <Option value="nombre_de_mtres_du_tampon" type="QString" name="component_description"/>
      <Option value="31.160846540726197" type="double" name="component_height"/>
      <Option value="168.58223930244674" type="double" name="component_pos_x"/>
      <Option value="440.1002683233015" type="double" name="component_pos_y"/>
      <Option value="200" type="double" name="component_width"/>
      <Option value="nombre_de_mtres_du_tampon" type="QString" name="name"/>
      <Option value="true" type="bool" name="outputs_collapsed"/>
      <Option value="true" type="bool" name="parameters_collapsed"/>
    </Option>
    <Option type="Map" name="parcellaire">
      <Option value="" type="QString" name="color"/>
      <Option type="Map" name="comment">
        <Option value="" type="QString" name="color"/>
        <Option value="" type="QString" name="component_description"/>
        <Option value="60" type="double" name="component_height"/>
        <Option value="426" type="double" name="component_pos_x"/>
        <Option value="279" type="double" name="component_pos_y"/>
        <Option value="100" type="double" name="component_width"/>
        <Option value="true" type="bool" name="outputs_collapsed"/>
        <Option value="true" type="bool" name="parameters_collapsed"/>
      </Option>
      <Option value="parcellaire" type="QString" name="component_description"/>
      <Option value="46.12331095875578" type="double" name="component_height"/>
      <Option value="169.2125944694138" type="double" name="component_pos_x"/>
      <Option value="242.77907056342636" type="double" name="component_pos_y"/>
      <Option value="189.58137499999998" type="double" name="component_width"/>
      <Option value="parcellaire" type="QString" name="name"/>
      <Option value="true" type="bool" name="outputs_collapsed"/>
      <Option value="true" type="bool" name="parameters_collapsed"/>
    </Option>
  </Option>
</Option>'''

    new_models_dir = r"C:\Users\Autreutilisateur\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\models"
    modified_content = replace_qml_paths_in_model_content(model_content, new_models_dir)
    
    expected_path = r"C:\Users\Autreutilisateur\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\models\Parcelles dans la zone.qml"
    assert expected_path in modified_content
    assert r"C:\Users\NoPiT\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\models\Parcelles dans la zone.qml" not in modified_content



def test_replace_qml_paths_real_life_simple():
    """Test with my file"""
    model_content = r'''<!DOCTYPE model>
<Option type="Map">
  <Option type="Map" name="children">
    <Option type="Map" name="native:setlayerstyle_1">
      <Option type="bool" name="active" value="true"/>
      <Option name="alg_config"/>
      <Option type="QString" name="alg_id" value="native:setlayerstyle"/>
      <Option type="QString" name="color" value=""/>
      <Option type="Map" name="comment">
        <Option type="QString" name="color" value=""/>
        <Option type="QString" name="component_description" value=""/>
        <Option type="double" name="component_height" value="60"/>
        <Option type="double" name="component_pos_x" value="320"/>
        <Option type="double" name="component_pos_y" value="115"/>
        <Option type="double" name="component_width" value="100"/>
        <Option type="bool" name="outputs_collapsed" value="true"/>
        <Option type="bool" name="parameters_collapsed" value="true"/>
      </Option>
      <Option type="QString" name="component_description" value="Appliquer le style"/>
      <Option type="double" name="component_height" value="30"/>
      <Option type="double" name="component_pos_x" value="432"/>
      <Option type="double" name="component_pos_y" value="178"/>
      <Option type="double" name="component_width" value="200"/>
      <Option name="dependencies"/>
      <Option type="QString" name="id" value="native:setlayerstyle_1"/>
      <Option name="outputs"/>
      <Option type="bool" name="outputs_collapsed" value="true"/>
      <Option type="bool" name="parameters_collapsed" value="true"/>
      <Option type="Map" name="params">
        <Option type="List" name="INPUT">
          <Option type="Map">
            <Option type="QString" name="parameter_name" value="vector_layer"/>
            <Option type="int" name="source" value="0"/>
          </Option>
        </Option>
        <Option type="List" name="STYLE">
          <Option type="Map">
            <Option type="int" name="source" value="2"/>
            <Option type="QString" name="static_value" value="C:\Users\NoPiT\Desktop\example_style_file.qml"/>
          </Option>
        </Option>
      </Option>
    </Option>
  </Option>
  <Option name="designerParameterValues"/>
  <Option name="groupBoxes"/>
  <Option name="help"/>
  <Option type="QString" name="internal_version" value="Version2"/>
  <Option name="modelVariables"/>
  <Option type="QString" name="model_group" value=""/>
  <Option type="QString" name="model_name" value="apply style"/>
  <Option type="QString" name="outputGroup" value=""/>
  <Option name="outputOrder"/>
  <Option type="Map" name="parameterDefinitions">
    <Option type="Map" name="vector_layer">
      <Option name="data_types"/>
      <Option type="invalid" name="default"/>
      <Option type="invalid" name="defaultGui"/>
      <Option type="QString" name="description" value="Vector layer"/>
      <Option type="int" name="flags" value="0"/>
      <Option type="QString" name="help" value=""/>
      <Option name="metadata"/>
      <Option type="QString" name="name" value="vector_layer"/>
      <Option type="QString" name="parameter_type" value="vector"/>
    </Option>
  </Option>
  <Option name="parameterOrder"/>
  <Option type="Map" name="parameters">
    <Option type="Map" name="vector_layer">
      <Option type="QString" name="color" value=""/>
      <Option type="Map" name="comment">
        <Option type="QString" name="color" value=""/>
        <Option type="QString" name="component_description" value=""/>
        <Option type="double" name="component_height" value="60"/>
        <Option type="double" name="component_pos_x" value="320"/>
        <Option type="double" name="component_pos_y" value="15"/>
        <Option type="double" name="component_width" value="100"/>
        <Option type="bool" name="outputs_collapsed" value="true"/>
        <Option type="bool" name="parameters_collapsed" value="true"/>
      </Option>
      <Option type="QString" name="component_description" value="vector_layer"/>
      <Option type="double" name="component_height" value="30"/>
      <Option type="double" name="component_pos_x" value="143"/>
      <Option type="double" name="component_pos_y" value="150"/>
      <Option type="double" name="component_width" value="200"/>
      <Option type="QString" name="name" value="vector_layer"/>
      <Option type="bool" name="outputs_collapsed" value="true"/>
      <Option type="bool" name="parameters_collapsed" value="true"/>
    </Option>
  </Option>
</Option>
'''

    new_models_dir = r"C:\Users\NoPiT\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\testm\models"
    modified_content = replace_qml_paths_in_model_content(model_content, new_models_dir)
    
    expected_path = r"C:\Users\NoPiT\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\testm\models\example_style_file.qml"
    assert expected_path in modified_content
    assert r"C:\Users\NoPiT\Desktop\example_style_file.qml" not in modified_content
