@echo off
:: 执行测试用例，生成Allure报告
pytest --alluredir=report --clean-alluredir -v
:: 启动Allure服务
allure serve report
:: 防止脚本执行完直接关闭窗口
pause