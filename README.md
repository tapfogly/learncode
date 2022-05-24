# AutoTest

基于 [pytest](https://docs.pytest.org/en/7.1.x/index.html) ,用于robokit和rdscore的自动化测试的脚本库

## 测试前需要配置的内容

- 需要在 [config.json](config.json) 中将 `rbk_ip` 和 `rdscore_ip` 配置正确。
- 需要安装[pytest](https://docs.pytest.org/en/7.1.x/index.html) 以及 [pytest-html](https://pytest-html.readthedocs.io/en/latest/index.html)
```
pip install -U pytest
```

```
pip install -U pytest-html
```

## 测试文件夹名称和文件名规则

pytest是python的第三方测试框架,是基于unittest的扩展框架,比unittest更简洁,更高效。使用pytest编写用例,必须遵守以下规则:

1. 测试文件名必须以“test_”开头或者"_test"结尾(如:test_ab.py)

2. 测试方法必须以“test_”开头。

3. 测试类命名以"Test"开头。

## 运行测试用例方式
- 测试rbk
```bash
pytest test_rbk -v --html=report.html --self-contained-html
```
- 测试rdscore
```bash
pytest test_rdscore -v --html=report.html --self-contained-html
```
最后测试结果在`report.html`中
