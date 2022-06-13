import socket
import requests
import webbrowser


class CodingLib:
    def __init__(self, *args: str):
        """
        使用OAuth2授权登录,传两个参数: [clientId, clientSecret]\n
        使用个人令牌登录,传一个参数: [token]

        :param clientId: OAuth2 认证 clientId
        :param clientSecret: OAuth2 认证 clientSecret
        :param token: 个人令牌 token
        """
        self.clientId = None
        self.clientSecret = None
        self.token = None
        self.headers = {"Content-Type": "application/json"}
        self.accessToken = None
        if len(args) == 2:
            self.clientId = args[0]
            self.clientSecret = args[1]
            self.getOAuth2Token()
        elif len(args) == 1:
            self.token = args[0]
            self.headers["Authorization"] = "token " + self.token
        else:
            raise Exception("参数错误")
        # coding统一api接口url
        self.apiUrl = 'https://e.coding.net/open-api'

    # 获取 access_token
    def getOAuth2Token(self):
        # 授权url
        accessUrl = f"https://seer-group.coding.net/oauth_authorize.html?" \
                    f"your-team=seer-group&client_id={self.clientId}&" \
                    f"redirect_uri=http://localhost:3000/callback&response_type=code"
        # 打开授权登录页面
        webbrowser.open(accessUrl)
        # socket实现简单http服务器,接收授权码
        httpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        httpServer.bind(('', 3000))
        httpServer.listen(1)
        sock, addr = httpServer.accept()
        recv = sock.recv(1024)
        params = recv.decode("ascii").split()[1].split('?')[1].split('&')
        code = None
        # 找出code
        for param in params:
            if param.startswith("code="):
                code = param.split('=')[1]
                break
        if code:
            sock.send(
                'HTTP/1.1 200 Authorization succeeded\r\nContent-Type: text/html\r\n\r\nAuthorization succeeded'.encode("ascii"))
        else:
            sock.send('HTTP/1.1 401 Authorization failed\r\nContent-Type: text/html\r\n\r\nAuthorization failed'.encode("ascii"))
        sock.close()
        if code:
            res = requests.post("https://seer-group.coding.net/api/oauth/access_token",
                                data={
                                    "your-team": "seer-group",
                                    "client_id": self.clientId,
                                    "client_secret": self.clientSecret,
                                    "code": code,
                                    "grant_type": "authorization_code",
                                })
            resJson = res.json()
            self.accessToken = resJson["access_token"]
            self.headers["Authorization"] = "Bearer " + self.accessToken

    # 获取用户信息
    def getUserInfo(self):
        if self.token:
            res = requests.get("https://seer-group.coding.net/api/me", headers=self.headers)
        else:
            res = requests.get("https://seer-group.coding.net/api/me?access_token=" + self.accessToken)
        return res

    # 获取项目内所有成员id
    def getProjectMemberIds(self, projectName: str):
        # 查询项目ID
        res = self.describeProjectByName(projectName)
        # 查询项目成员
        res = self.describeProjectMembers(res.json()["Response"]["Project"]["Id"], 1, 1000)
        # 成员字典
        memberIds = {}
        for i in res.json()["Response"]["Data"]["ProjectMembers"]:
            memberIds[i["Id"]] = i["Name"]
        return memberIds

    # 生成markdown
    @staticmethod
    def generateMarkdown(title: str, content: str, d: dict):
        # 标题
        md = f"### {title}\n\n---\n\n"
        # 内容
        md += f"{content}\n\n"
        # 表
        md += "| Key | Value |\n| :--- | :--- |\n"
        for key, value in d.items():
            md += f"| {key} | {value} |\n"
        return md

    ####################################################################################################################
    #                                                                                                                  #
    #                                            以下是 CODING 的 API　                                                  #
    #                                                                                                                  #
    ####################################################################################################################

    # 查询团队内所有项目列表
    def describeCodingProjects(self, pageNumber=1, pageSize=10, projectName=None):
        d = {"Action": "DescribeCodingProjects", "PageNumber": pageNumber, "PageSize": pageSize}
        if projectName:
            d["ProjectName"] = projectName
        return requests.post(self.apiUrl + "?Action=DescribeCodingProjects", json=d, headers=self.headers)

    # 查询团队成员列表
    def describeTeamMembers(self, pageNumber=1, pageSize=10):
        d = {"Action": "DescribeTeamMembers", "PageNumber": pageNumber, "PageSize": pageSize}
        return requests.post(self.apiUrl + "?Action=DescribeTeamMembers", json=d, headers=self.headers)

    # # 创建项目
    # def createCodingProject(self):
    #     pass
    #
    # # 编辑项目
    # def modifyProject(self):
    #     pass
    #
    # # 删除项目
    # def deleteOneProject(self):
    #     pass
    #
    # # 查询项目根据项目id
    # def describeOneProject(self):
    #     pass
    #
    # 查询项目根据项目名称
    def describeProjectByName(self, projectName: str):
        d = {"Action": "DescribeProjectByName", "ProjectName": projectName}
        return requests.post(self.apiUrl + "?Action=DescribeProjectByName", json=d, headers=self.headers)

    # # 查询项目成员列表
    def describeProjectMembers(self, projectId: int, pageNumber=1, pageSize=10, roleId: int = None):
        d = {"Action": "DescribeProjectMembers", "PageNumber": pageNumber, "PageSize": pageSize, "ProjectId": projectId}
        if roleId:
            d["RoleId"] = roleId
        return requests.post(self.apiUrl + "?Action=DescribeProjectMembers", json=d, headers=self.headers)

    # # 项目成员添加
    # def createProjectMember(self):
    #     pass
    #
    # # 查询成员所在的项目列表
    # def describeUserProjects(self):
    #     pass
    #
    # 获取用户个人信息
    def describeCodingCurrentUser(self):
        d = {"Action": "DescribeCodingCurrentUser"}
        return requests.post(self.apiUrl + "?Action=DescribeCodingCurrentUser", json=d, headers=self.headers)

    # # 配置项目成员权限
    # def modifyProjectPermission(self):
    #     pass
    #
    # # 查询项目用户组
    # def describeProjectRoles(self):
    #     pass
    #
    # # 查询需求关联事项列表
    # def describeRequirementDefectRelation(self):
    #     pass
    #
    # # 修改缺陷所属的需求
    # def modifyDefectRelatedRequirement(self):
    #     pass
    #
    # # 需求关联缺陷
    # def createRequirementDefectRelation(self):
    #     pass

    # 创建事项
    def createIssue(self, projectName: str, type: str, name: str, priority: str, startDate: str, dueDate: str,
                    **kwargs):
        d = {"Action": "CreateIssue", "ProjectName": projectName, "Type": type, "Name": name, "Priority": priority,
             "StartDate": startDate, "DueDate": dueDate}
        d.update(kwargs)
        return requests.post(self.apiUrl + "?Action=CreateIssue", json=d, headers=self.headers)

    # 删除事项
    def deleteIssue(self, projectName: str, issueCode: int, issueType: str = None):
        d = {"Action": "DeleteIssue", "ProjectName": projectName, "IssueCode": issueCode}
        if issueType:
            d["IssueType"] = issueType
        return requests.post(self.apiUrl + "?Action=DeleteIssue", json=d, headers=self.headers)

    # 查询事项附件的下载地址
    def describeIssueFileUrl(self, projectName: str, fileld: int):
        d = {"Action": "DescribeIssueFileUrl", "ProjectName": projectName, "Fileld": fileld}
        return requests.post(self.apiUrl + "?Action=DescribeIssueFileUrl", json=d, headers=self.headers)

    # 查询筛选器列表
    def describeIssueFilterList(self, projectName: str, IssueType: str):
        d = {"Action": "DescribeIssueFilterList", "ProjectName": projectName, "IssueType": IssueType}
        return requests.post(self.apiUrl + "?Action=DescribeIssueFilterList", json=d, headers=self.headers)

    # 查询事项列表（旧）
    def describeIssueList(self, **kwargs):
        return requests.post(self.apiUrl + "?Action=DescribeIssueList", json=kwargs, headers=self.headers)

    # 查询事项详情
    def describeIssue(self, projectName: str, issueCode: int):
        d = {"Action": "DescribeIssue", "ProjectName": projectName, "IssueCode": issueCode}
        return requests.post(self.apiUrl + "?Action=DescribeIssue", json=d, headers=self.headers)

    # 查询属性设置
    def describeProjectIssueFieldList(self, projectName: str, issueTypeId: int = None, issueType: str = None):
        if issueType or issueTypeId:
            d = {"Action": "DescribeProjectIssueFieldList", "ProjectName": projectName}
            if issueType:
                d["IssueType"] = issueType
            elif issueTypeId:
                d["IssueTypeId"] = issueTypeId
            return requests.post(self.apiUrl + "?Action=DescribeProjectIssueFieldList", json=d, headers=self.headers)
        else:
            raise Exception("issueType or issueTypeId is required")

    # 查询状态设置
    def describeProjectIssueStatusList(self, projectName: str, issueTypeId: int = None, issueType: str = None):
        if issueType or issueTypeId:
            d = {"Action": "DescribeProjectIssueStatusList", "ProjectName": projectName}
            if issueType:
                d["IssueType"] = issueType
            elif issueTypeId:
                d["IssueTypeId"] = issueTypeId
            return requests.post(self.apiUrl + "?Action=DescribeProjectIssueStatusList", json=d, headers=self.headers)

    # 修改事项
    def modifyIssue(self, projectName: str, issueCode: int, name: str, **kwargs):
        d = {"Action": "ModifyIssue", "ProjectName": projectName, "IssueCode": issueCode, "Name": name}
        d.update(kwargs)
        return requests.post(self.apiUrl + "?Action=ModifyIssue", json=d, headers=self.headers)

    # 修改事项描述
    def modifyIssueDescription(self, projectName: str, issueCode: int, description: str):
        d = {"Action": "ModifyIssueDescription", "ProjectName": projectName, "IssueCode": issueCode,
             "Description": description}
        return requests.post(self.apiUrl + "?Action=ModifyIssueDescription", json=d, headers=self.headers)

    # 查询后置事项
    def describeBlockIssueList(self, projectName: str, issueCode: int):
        d = {"Action": "DescribeBlockIssueList", "ProjectName": projectName, "IssueCode": issueCode}
        return requests.post(self.apiUrl + "?Action=DescribeBlockIssueList", json=d, headers=self.headers)

    # 查询前置事项
    def describeBlockedByIssueList(self, projectName: str, issueCode: int):
        d = {"Action": "DescribeBlockedByIssueList", "ProjectName": projectName, "IssueCode": issueCode}
        return requests.post(self.apiUrl + "?Action=DescribeBlockedByIssueList", json=d, headers=self.headers)

    # 查询子事项列表
    def describeSubIssueList(self, projectName: str, issueCode: int):
        d = {"Action": "DescribeSubIssueList", "ProjectName": projectName, "IssueCode": issueCode}
        return requests.post(self.apiUrl + "?Action=DescribeSubIssueList", json=d, headers=self.headers)

    # 删除前置事项
    def deleteIssueBlock(self, projectName: str, issueCode: int, blockIssueCode: int):
        d = {"Action": "DeleteIssueBlock", "ProjectName": projectName, "IssueCode": issueCode,
             "BlockIssueCode": blockIssueCode}
        return requests.post(self.apiUrl + "?Action=DeleteIssueBlock", json=d, headers=self.headers)

    # 添加前置事项
    def createIssueBlock(self, projectName: str, issueCode: int, blockIssueCode: int):
        d = {"Action": "CreateIssueBlock", "ProjectName": projectName, "IssueCode": issueCode,
             "BlockIssueCode": blockIssueCode}
        return requests.post(self.apiUrl + "?Action=CreateIssueBlock", json=d, headers=self.headers)

    # 修改事项父需求
    def modifyIssueParentRequirement(self, projectName: str, issueCode: int, ParentIssueCode: int):
        d = {"Action": "ModifyIssueParentRequirement", "ProjectName": projectName, "IssueCode": issueCode,
             "ParentIssueCode": ParentIssueCode}
        return requests.post(self.apiUrl + "?Action=ModifyIssueParentRequirement", json=d, headers=self.headers)

    # 查询企业所有事项类型列表
    def describeTeamIssueTypeList(self):
        d = {"Action": "DescribeTeamIssueTypeList"}
        return requests.post(self.apiUrl + "?Action=DescribeTeamIssueTypeList", json=d, headers=self.headers)

    # 查询项目引用的事项类型列表
    def describeProjectIssueTypeList(self, projectName: str):
        d = {"Action": "DescribeProjectIssueTypeList", "ProjectName": projectName}
        return requests.post(self.apiUrl + "?Action=DescribeProjectIssueTypeList", json=d, headers=self.headers)

    # 事项列表（新）
    def describeIssueListWithPage(self, projectName: str, issueType: str, pageNumber: int, pageSize: int,
                                  Conditions: list = None, sortKey: str = None, sortValue: str = None):
        d = {"Action": "DescribeIssueListWithPage", "ProjectName": projectName, "IssueType": issueType,
             "PageNumber": pageNumber, "PageSize": pageSize}
        if Conditions:
            d["Conditions"] = Conditions
        if sortKey:
            d["SortKey"] = sortKey
        if sortValue:
            d["SortValue"] = sortValue
        return requests.post(self.apiUrl + "?Action=DescribeIssueListWithPage", json=d, headers=self.headers)

    # 事项关联的测试用例
    def describeRelatedCaseList(self, projectName: str, issueCode: int):
        d = {"Action": "DescribeRelatedCaseList", "ProjectName": projectName, "IssueCode": issueCode}
        return requests.post(self.apiUrl + "?Action=DescribeRelatedCaseList", json=d, headers=self.headers)

    # 创建事项评论
    def createIssueComment(self, projectName: str, issueCode: int, content: str, ParentId: int = None):
        d = {"Action": "CreateIssueComment", "ProjectName": projectName, "IssueCode": issueCode, "Content": content}
        if ParentId:
            d["ParentId"] = ParentId
        return requests.post(self.apiUrl + "?Action=CreateIssueComment", json=d, headers=self.headers)

    # 修改事项评论
    def modifyIssueComment(self, projectName: str, issueCode: int, commentId: int, content: str):
        d = {"Action": "ModifyIssueComment", "ProjectName": projectName, "IssueCode": issueCode, "CommentId": commentId,
             "Content": content}
        return requests.post(self.apiUrl + "?Action=ModifyIssueComment", json=d, headers=self.headers)

    # 查询事项评论列表
    def describeIssueCommentList(self, projectName: str, issueCode: int):
        d = {"Action": "DescribeIssueCommentList", "ProjectName": projectName, "IssueCode": issueCode}
        return requests.post(self.apiUrl + "?Action=DescribeIssueCommentList", json=d, headers=self.headers)

    # 获取事项的状态变更历史
    def describeIssueStatusChangeLogList(self, projectName: str, issueCode: list[int]):
        d = {"Action": "DescribeIssueStatusChangeLogList", "ProjectName": projectName, "IssueCode": issueCode}
        return requests.post(self.apiUrl + "?Action=DescribeIssueStatusChangeLogList", json=d, headers=self.headers)

    # # 创建迭代
    # def createIteration(self):
    #     pass
    #
    # # 删除迭代
    # def deleteIteration(self):
    #     pass
    #
    # # 迭代详情
    # def describeIteration(self):
    #     pass
    #
    # # 迭代列表
    # def describeIterationList(self):
    #     pass
    #
    # # 修改迭代
    # def modifyIteration(self):
    #     pass
    #
    # # 批量规划迭代
    # def planIterationIssue(self):
    #     pass
    #
    # # 查询工时日志列表
    # def describeIssueWorkLogList(self):
    #     pass
    #
    # # 登记工时
    # def createIssueWorkHours(self):
    #     pass
    #
    # # 删除工时日志
    # def deleteIssueWorkHours(self):
    #     pass
    #
    # # 创建代码仓库
    # def createGitDepot(self):
    #     pass
    #
    # # 获取代码仓库详情
    # def describeGitDepot(self):
    #     pass
    #
    # # 删除代码仓库
    # def deleteGitDepot(self):
    #     pass
    #
    # # 修改仓库描述
    # def modifyDepotDescription(self):
    #     pass
    #
    # # 修改仓库名称
    # def modifyDepotName(self):
    #     pass
    #
    # # 创建提交注释
    # def createGitCommitNote(self):
    #     pass
    #
    # # 查询项目下仓库信息列表
    # def describeProjectDepotInfoList(self):
    #     pass
    #
    # # 获取团队下仓库列表
    # def describeTeamDepotInfoList(self):
    #     pass
    #
    # # 修改仓库默认分支
    # def modifyDefaultBranch(self):
    #     pass
    #
    # # 根据模板创建仓库
    # def createDepotByTemplate(self):
    #     pass
    #
    # # 查询仓库目录下文件和文件夹名字
    # def describeGitFiles(self):
    #     pass
    #
    # # 获取文件详情
    # def describeGitFile(self):
    #     pass
    #
    # # 导入用户 SSH 公钥
    # def createSshKey(self):
    #     pass
    #
    # # 获取当前用户 SSH 公钥
    # def describeSshKey(self):
    #     pass
    #
    # # 删除当前用户的 SSH 公钥
    # def deleteSshKey(self):
    #     pass
    #
    # # 为团队成员添加 SSH 公钥
    # def createMemberSshKey(self):
    #     pass
    #
    # # 查询团队成员的 SSH 公钥列表
    # def describeMemberSshKey(self):
    #     pass
    #
    # # 删除团队成员的 SSH 公钥
    # def deleteMemberSshKey(self):
    #     pass


if __name__ == '__main__':
    cd = CodingLib("")
    memberIds = cd.getProjectMemberIds("test_center")
    with open("测试中心成员ID.txt", "w", encoding="utf-8") as f:
        for k, v in memberIds.items():
            f.write(f"{k}:{v}\n")