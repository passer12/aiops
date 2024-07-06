from sparkAPI.IntelligentOps.sparkdesk_api.core import SparkAPI
import sys
import os

import re

def extract_code_review(message):
    """
    从给定的代码评审消息中提取评分、评价和建议。

    参数:
    message (str): 包含代码评审信息的字符串

    返回:
    dict: 包含'score'、'evaluation'和'suggestion'的字典
    """
    # 提取评分
    score = re.search(r'评分为：(\d+)', message)
    score = int(score.group(1)) if score else None

    # 提取评价
    evaluation = re.search(r'代码评价：(.*?)改进建议', message, re.DOTALL)
    evaluation = evaluation.group(1).strip() if evaluation else None

    # 提取建议
    suggestion = re.search(r'改进建议：(.*)', message, re.DOTALL)
    suggestion = suggestion.group(1).strip() if suggestion else None

    return {
        'score': score,
        'evaluations': evaluation,
        'suggestions': suggestion
    }


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
    
    def score_readability(self, code):
        """
        评估代码的可读性，返回可读性分数。
        """
        query = "评分区间0-10，请你评估下方代码的可读性，返回可读性分数，代码如下:\n" + code
        response_template = """
        回答模板为：
        “评分为：score
        代码评价：evaluations
        改进建议：suggestions”
        """ 
        query = query + response_template
        query_result = self.ai_tool.chat(query)
        # 在回答中提取分数
        result = extract_code_review(query_result)
        print(query_result)
        print(result)
        if result['score'] == None:
            result['score'] = 0
        if result['evaluations'] == None:
            result['evaluations'] = "No"
        if result['suggestions'] == None:
            result['suggestions'] = "No"
        
        # result = {
        #     "score": 5,
        #     "evaluations": 'hhha',
        #     "suggestions": 'hhha'
        # }
        return result
    
    def score_performance(self, code):
        """
        评估代码的性能，返回性能分数。
        """
        query = "评分区间0-10，请你评估下方代码的性能，返回性能分数，代码如下:\n" + code
        response_template = """
        回答模板为：
        “评分为：score
        代码评价：evaluations
        改进建议：suggestions”
        """ 
        query = query + response_template
        query_result = self.ai_tool.chat(query)
        # 在回答中提取分数
        result = extract_code_review(query_result)
        print(query_result)
        print(result)
        if result['score'] == None:
            result['score'] = 0
        if result['evaluations'] == None:
            result['evaluations'] = "No"
        if result['suggestions'] == None:
            result['suggestions'] = "No"
            
        # result = {
        #     "score": 5,
        #     "evaluations": 'hhha',
        #     "suggestions": 'hhha'
        # }
        
        return result
    
    def score_usability(self, code):
        """
        评估代码的可用性，返回可用性分数。
        """
        query = "评分区间0-10，请你评估下方代码的可用性，返回可用性分数，代码如下:\n" + code
        response_template = """
        回答模板为：
        “评分为：score
        代码评价：evaluations
        改进建议：suggestions”
        """ 
        query = query + response_template
        query_result = self.ai_tool.chat(query)
        # 在回答中提取分数
        result = extract_code_review(query_result)
        print(query_result)
        print(result)
        if result['score'] == None:
            result['score'] = 0
        if result['evaluations'] == None:
            result['evaluations'] = "No"
        if result['suggestions'] == None:
            result['suggestions'] = "No"
        
        # result = {
        #     "score": 5,
        #     "evaluations": 'hhha',
        #     "suggestions": 'hhha'
        # }
        
        return result
    
    def score_security(self, code):
        """
        评估代码的安全性，返回安全性分数。
        """
        query = "评分区间0-10，请你评估下方代码的安全性，返回安全性分数，代码如下:\n" + code
        response_template = """
        回答模板为：
        “评分为：score
        代码评价：evaluations
        改进建议：suggestions”
        """ 
        query = query + response_template
        query_result = self.ai_tool.chat(query)
        # 在回答中提取分数
        result = extract_code_review(query_result)
        print(query_result)
        print(result)
        if result['score'] == None:
            result['score'] = 0
        if result['evaluations'] == None:
            result['evaluations'] = "No"
        if result['suggestions'] == None:
            result['suggestions'] = "No"
        
        # result = {
        #     "score": 5,
        #     "evaluations": 'hhha',
        #     "suggestions": 'hhha'
        # }
        
        return result
    
    def score_maintainability(self, code):
        """
        评估代码的可维护性，返回可维护性分数。
        """
        query = "评分区间0-10，请你评估下方代码的可维护性，返回可维护性分数，代码如下:\n" + code
        response_template = """
        回答模板为：
        “评分为：score
        代码评价：evaluations
        改进建议：suggestions”
        """ 
        query = query + response_template
        query_result = self.ai_tool.chat(query)
        # 在回答中提取分数
        result = extract_code_review(query_result)
        print(query_result)
        print(result)
        if result['score'] == None:
            result['score'] = 0
        if result['evaluations'] == None:
            result['evaluations'] = "No"
        if result['suggestions'] == None:
            result['suggestions'] = "No"
        
        # result = {
        #     "score": 5,
        #     "evaluations": 'hhha',
        #     "suggestions": 'hhha'
        # }
        
        return result

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
        # file_info = "file_info"
        # evaluation_report = "evaluation_report"
        # issues = "issues"
        # optimization_suggestions = "optimization_suggestions"
        
        # 可读性
        readability_data = self.code_analysis_tool.score_readability(code)
        readability_score = readability_data["score"]
        readability_evaluations = readability_data["evaluations"]
        readability_suggestions = readability_data["suggestions"]
        # 性能
        performance_data = self.code_analysis_tool.score_performance(code)
        performance_score = performance_data["score"]
        performance_evaluations = performance_data["evaluations"]
        performance_suggestions = performance_data["suggestions"]
        # 可用性
        usability_data = self.code_analysis_tool.score_usability(code)
        usability_score = usability_data["score"]
        usability_evaluations = usability_data["evaluations"]
        usability_suggestions = usability_data["suggestions"]
        # 安全性
        security_data = self.code_analysis_tool.score_security(code)
        security_score = security_data["score"]
        security_evaluations = security_data["evaluations"]
        security_suggestions = security_data["suggestions"]
        # 可维护性
        maintainability_data = self.code_analysis_tool.score_maintainability(code)
        maintainability_score = maintainability_data["score"]
        maintainability_evaluations = maintainability_data["evaluations"]
        maintainability_suggestions = maintainability_data["suggestions"]
        
        # output_result = "Evaluation Report: \n" + evaluation_report + "\n\n" + "Issues: \n" + issues + "\n\n" + "Optimization Suggestions: \n" + optimization_suggestions
        output_result_dict = {
            "file_info":str(file_info), 
            "quality": str(evaluation_report), 
            "issues": str(issues), 
            "suggestions": str(optimization_suggestions),
            "nodescore":{
                "readability": {
                    "score": readability_score,
                    "evaluations": readability_evaluations,
                    "suggestions": readability_suggestions
                },
                "performance": {
                    "score": performance_score,
                    "evaluations": performance_evaluations,
                    "suggestions": performance_suggestions
                },
                "usability": {
                    "score": usability_score,
                    "evaluations": usability_evaluations,
                    "suggestions": usability_suggestions
                },
                "security": {
                    "score": security_score,
                    "evaluations": security_evaluations,
                    "suggestions": security_suggestions
                },
                "maintainability": {
                    "score": maintainability_score,
                    "evaluations": maintainability_evaluations,
                    "suggestions": maintainability_suggestions
                }
            }            
        }
        # print(output_result_dict)
        
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