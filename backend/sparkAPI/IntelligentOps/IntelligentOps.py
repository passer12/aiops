from sparkdesk_api.core import SparkAPI
import sys
import os

# # 获取上级目录的路径
# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# # 将上级目录添加到sys.path中
# sys.path.append(parent_dir)
# # 导入上级目录中的utils模块
# import utils

app_id="e8bd2492"
api_secret="MGY1MjIzMDk1MTQ4Y2U1YzUxMWI5Yzk1"
api_key="28b98e55ec8e83daddf1e591952e2614"

class CodeAnalysisTool:
    def __init__(self):
        self.ai_tool = SparkAPI(
        app_id=app_id,
        api_secret=api_secret,
        api_key=api_key,
        # version=2.1
        # assistant_id="xyzspsb4i5s7_v1"
    )

    def analyze_repo_structure(self, structure):
        """
        分析仓库结构，返回仓库结构的分析结果与建议。
        """
        query = "分析下面的仓库结构，进行评估并给出建议。仓库结构如下:\n" + structure
        query_result = self.ai_tool.chat(query)
        return query_result
    
    def analyze_file_info(self, file_content):
        """
        分析文件信息，返回文件信息的分析结果。
        """
        query = "分析下面的文件，给出简要的文件信息介绍。文件信息如下:\n" + file_content
        query_result = self.ai_tool.chat(query)
        return query_result
    
    def analyze_issues(self, code):
        """
        分析代码，识别潜在问题，并返回问题列表。
        """
        query = "分析下面的代码，识别潜在问题，并返回问题列表，代码如下:\n" + code
        query_result = self.ai_tool.chat(query)
        return query_result

    def evaluate_quality(self, code):
        """
        评估代码质量，生成评估报告，并返回报告内容。
        """
        query = "评估代码质量，生成评估报告，代码如下:\n" + code
        query_result = self.ai_tool.chat(query)
        return query_result
    
    def generate_suggestions(self, code, issue):
        """
        根据代码质量问题生成优化建议，并返回建议列表。
        """
        query = "根据代码质量问题生成优化建议，问题如下:\n" + issue + "原代码如下：\n" + code
        query_result = self.ai_tool.chat(query)
        return query_result

class IntelligentOps:
    # 初始化
    def __init__(self, code_analysis_tool):
        self.code_analysis_tool = code_analysis_tool
    
    # 代码处理
    def code_processing(self, file_path):
        """
        对代码进行处理，如格式化、去除注释等。
        """    
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
            return code
        except Exception as e:
            return str(e)

    # 分析代码问题
    def analyze_code_issues(self, code):
        """
        对提交的代码进行问题分析，识别潜在问题。
        """
        analysis_result = self.code_analysis_tool.analyze_issues(code)
        return analysis_result

    # 评估代码质量
    def evaluate_code_quality(self, code):
        """
        评估代码的质量，生成评估报告，并返回报告内容。
        """
        evaluation_report = self.code_analysis_tool.evaluate_quality(code)
        return evaluation_report

    # 生成优化建议
    def generate_suggestions(self, code, issues):
        """
        根据代码质量问题生成优化建议，并返回建议。
        """
        optimization_suggestions = self.code_analysis_tool.generate_suggestions(code, issues)
        return optimization_suggestions

    # 质量评估、问题分许、建议生成
    def quality_issues_suggestions(self, code):
        """
        对提交的代码进行分析、评估、建议，返回分析结果、评估报告、优化建议。
        """
        file_info = self.code_analysis_tool.analyze_file_info(code)
        evaluation_report = self.evaluate_code_quality(code)
        issues = self.analyze_code_issues(code)
        optimization_suggestions = self.generate_suggestions(code, issues)
        # output_result = "Evaluation Report: \n" + evaluation_report + "\n\n" + "Issues: \n" + issues + "\n\n" + "Optimization Suggestions: \n" + optimization_suggestions
        output_result_dict = {"file_info":str(file_info), "quality": str(evaluation_report), "issues": str(issues), "suggestions": str(optimization_suggestions)}
        return output_result_dict

    def repo_analysis(self, repo_path):
        """
        对仓库进行代码分析，返回分析结果、评估报告、优化建议。
        """
        # structure, contents = utils.read_directory(repo_path)
        # 仓库结构
        # directory_structure_string = utils.build_structure_string(structure)
        contents = {"file1": "content1", "file2": "content2", "file3": "content3"}
        directory_structure_string = "dir1\n  dir2\n    file1\n    file2\n  file3\n"
        
        repo_structure_analysis_result = self.code_analysis_tool.analyze_repo_structure(directory_structure_string)

        # 代码分析、评估、建议
        code_analysis_result = ""
        for file_path, content in contents.items():
            code_string = ""
            # code_string += f"{file_path}: \n"
            code_string += content
            code_analysis_result += f"{file_path} analysis result: \n" + self.quality_issues_suggestions(code_string) + "\n\n"
        
        return "repo structure analysis result: \n" + repo_structure_analysis_result + "\n\n" + "code analysis result: \n" + code_analysis_result + "\n\n"
    
    def repo_analysis_url(self, repo_url):
        """
        对仓库进行代码分析，返回分析结果、评估报告、优化建议。
        """
        # structure, contents = utils.read_directory(repo_path)
        # 仓库结构
        # directory_structure_string = utils.build_structure_string(structure)
        contents = {"file1": "content1", "file2": "content2", "file3": "content3"}
        directory_structure_string = "dir1\n  dir2\n    file1\n    file2\n  file3\n"
        
        repo_structure_analysis_result = self.code_analysis_tool.analyze_repo_structure(directory_structure_string)

        # 代码分析、评估、建议
        code_analysis_result = ""
        for file_path, content in contents.items():
            code_string = ""
            # code_string += f"{file_path}: \n"
            code_string += content
            code_analysis_result += f"{file_path} analysis result: \n" + self.quality_issues_suggestions(code_string) + "\n\n"
        
        return "repo structure analysis result: \n" + repo_structure_analysis_result + "\n\n" + "code analysis result: \n" + code_analysis_result + "\n\n"
    
    # 日志记录
    def _log_exception(self, exception):
        """
        内部方法，记录异常日志。
        """
        # Placeholder, actual logging implementation needed
        pass

if __name__ == '__main__':

    code_analysis_tool = CodeAnalysisTool()
    intelligent_ops = IntelligentOps(code_analysis_tool)

    # 代码分析    
    code = intelligent_ops.code_processing("../spark-test-code.py")
    print(intelligent_ops.quality_issues_suggestions(code))
    
    # 仓库分析
    print(intelligent_ops.repo_analysis("../githubapi-test-repo"))