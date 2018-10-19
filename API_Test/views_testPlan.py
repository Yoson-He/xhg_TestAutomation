import xml.etree.ElementTree as ET


def create_plan(plan_name):
    txt = '<?xml version="1.0" encoding="UTF-8"?>' \
          '<jmeterTestPlan version="1.2" properties="4.0" jmeter="4.0 r1823414">' \
          ' <hashTree>' \
          '     <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="测试计划" enabled="true">' \
          '         <stringProp name="TestPlan.comments"></stringProp>' \
          '             <boolProp name="TestPlan.functional_mode">false</boolProp>' \
          '             <boolProp name="TestPlan.tearDown_on_shutdown">true</boolProp>' \
          '             <boolProp name="TestPlan.serialize_threadgroups">true</boolProp>' \
          '             <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">' \
          '                 <collectionProp name="Arguments.arguments">' \
          '                     <elementProp name="QQ" elementType="Argument">' \
          '                         <stringProp name="Argument.name">QQ</stringProp>' \
          '                         <stringProp name="Argument.value">EEEE</stringProp>' \
          '                         <stringProp name="Argument.metadata">=</stringProp>' \
          '                     </elementProp>' \
          '                 </collectionProp>' \
          '             </elementProp>' \
          '             <stringProp name="TestPlan.user_define_classpath"></stringProp>' \
          '     </TestPlan>' \
          '     <hashTree>' \
          ' </hashTree >'\
          '</jmeterTestPlan >'
        #创建根节点
    jmeterTestPlan = ET.Element("jmeterTestPlan")
    jmeterTestPlan.attrib = {"version": "1.2", "properties": "4.0", "jmeter": "4.0 r1823414"}
    #创建子节点，并添加属性
    b = ET.SubElement(jmeterTestPlan,"sub1")
    b.attrib = {"name":"name attribute"}
    #创建子节点，并添加数据
    c = ET.SubElement(jmeterTestPlan,"sub2")
    c.text = "test"

    #创建elementtree对象，写文件
    tree = ET.ElementTree(jmeterTestPlan)
    tree.write(plan_name+".jmx")


#create_plan("test")

def aa():
    tt = """<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="4.0" jmeter="4.0 r1823414">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="测试计划" enabled="true">
      <stringProp name="TestPlan.comments"></stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.tearDown_on_shutdown">true</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">true</boolProp>
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
        <collectionProp name="Arguments.arguments">
          <elementProp name="QQ" elementType="Argument">
            <stringProp name="Argument.name">QQ</stringProp>
            <stringProp name="Argument.value">EEEE</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
        </collectionProp>
      </elementProp>
      <stringProp name="TestPlan.user_define_classpath"></stringProp>
    </TestPlan>
    <hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>"""

    with open("aa.xml", "w") as f:
        f.write(tt)


aa()

