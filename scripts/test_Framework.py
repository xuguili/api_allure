import requests,pytest,jsonpath,os
from xToolkit import xfile
from string import Template

#从文件读出所有行
case_data = xfile.read('../test_data/模拟接口测试用例.xls').excel_to_dict(sheet=1)

dic={}
@pytest.mark.parametrize("case_info",case_data)
def test_demo(case_info):

    url=case_info["接口URL"]

    if '$' in url:
        url = Template(url).substitute(dic) #将url中${token}替换为token具体值 dic["key"]=value

    params=eval(case_info["URL参数"]) #eval去除前后\n
    method=case_info["请求方式"]
    data=eval(case_info["JSON参数"])
    res = requests.request(url=url,method=method,params=params,data=data)

    if case_info["提取参数"]:
        lst = jsonpath.jsonpath(res.json(),"$.."+case_info["提取参数"]) #获取token值

        dic[case_info["提取参数"]]=lst[0]

    assert case_info["预期状态码"]==res.status_code







