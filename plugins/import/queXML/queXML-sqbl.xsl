<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xsi:schemaLocation="sqbl:1 https://raw.github.com/LegoStormtroopr/sqbl-schema/master/Schemas/sqbl.xsd"
    xmlns:sqbl="sqbl:1" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xhtml="http://www.w3.org/1999/xhtml"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" exclude-result-prefixes="xhtml xsl" version="1.0">

    <xsl:output method="xml" indent="yes" />

    <xsl:param name="prefered-lang">en</xsl:param>

    <xsl:template match="/questionnaire">
        <sqbl:QuestionModule version="1" name="qImport_{@id}" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="sqbl:1 https://raw.github.com/LegoStormtroopr/sqbl-schema/master/Schemas/sqbl.xsd">
            <sqbl:TextComponents>
                <sqbl:TextComponent xml:lang="en">
                    <sqbl:LongName>
                        <xsl:value-of select="title" />
                    </sqbl:LongName>
                    <sqbl:Title>
                        <xsl:value-of select="title" />
                    </sqbl:Title>
                </sqbl:TextComponent>
            </sqbl:TextComponents>
            <sqbl:ModuleLogic>
                <xsl:apply-templates select="questionnaireInfo[position/text()='before']" />
                <xsl:apply-templates select="section" />
                <xsl:apply-templates select="questionnaireInfo[position/text()='after']" />
            </sqbl:ModuleLogic>
        </sqbl:QuestionModule>
    </xsl:template>

    <xsl:template match="questionnaireInfo">
        <sqbl:Statement name="qi_{position/text()}_{position()}">
            <sqbl:TextComponent xml:lang="en">
                <sqbl:StatementText>
                    <xsl:value-of select="text" />
                </sqbl:StatementText>
            </sqbl:TextComponent>
        </sqbl:Statement>
    </xsl:template>
    <xsl:template match="section">
        <xsl:apply-templates select="sectionInfo[position/text()='before']" />
        <xsl:apply-templates select="sectionInfo[position/text()='title']" />
        <xsl:apply-templates select="question" />
        <xsl:apply-templates select="sectionInfo[position/text()='after']" />
    </xsl:template>
    <xsl:template match="sectionInfo">
        <sqbl:Statement name="sec_{position/text()}_{position()}">
            <sqbl:TextComponent xml:lang="en">
                <sqbl:StatementText>
                    <xsl:value-of select="text" />
                </sqbl:StatementText>
            </sqbl:TextComponent>
        </sqbl:Statement>
    </xsl:template>

    <xsl:template match="question">
        <xsl:variable name="id">
            <xsl:choose>
                <xsl:when test="@id">
                    <xsl:value-of select="@id" />
                </xsl:when>
                <xsl:when test="count(response)=1">
                    <xsl:value-of select="response/@varName" />
                </xsl:when>
                <xsl:when test="count(response)>1">
                    <xsl:value-of select="response/@varName" />
                </xsl:when>
            </xsl:choose>
        </xsl:variable>
        <sqbl:Question name="{$id}">
            <sqbl:TextComponent xml:lang="en">
                <sqbl:QuestionText>
                    <xsl:for-each select="text">
                        <xsl:value-of select="." />
                        <xsl:text> </xsl:text>
                    </xsl:for-each>
                </sqbl:QuestionText>
                <xsl:if test="directive">
                <sqbl:Instruction>
                    <xsl:for-each select="directive">
                        <xsl:value-of select="text" />
                        <xsl:text> </xsl:text>
                    </xsl:for-each>
                </sqbl:Instruction>
                </xsl:if>
            </sqbl:TextComponent>
            <sqbl:ResponseType>
                <xsl:apply-templates select="response"/>
            </sqbl:ResponseType>
            <xsl:if test="subQuestion">
                <sqbl:SubQuestions>
                    <xsl:apply-templates select="subQuestion"/>
                </sqbl:SubQuestions>
            </xsl:if>
        </sqbl:Question>
    </xsl:template>
    <xsl:template match="subQuestion">
        <sqbl:SubQuestion>
            <sqbl:TextComponent xml:lang="en">
                <xsl:value-of select="." />
            </sqbl:TextComponent>
        </sqbl:SubQuestion>
    </xsl:template>
    
    <xsl:template match="response[free/format/text()='integer'] | response[free/format/text()='currency']">
        <sqbl:Number>
            <xsl:if test="free/label">
                <sqbl:Prefix>
                    <sqbl:TextComponent xml:lang="en"><xsl:value-of select="free/label"/></sqbl:TextComponent>
                </sqbl:Prefix>
            </xsl:if>
            <xsl:if test="min">
                <sqbl:Minimum value="{min/text()}"/>
            </xsl:if>
            <xsl:if test="max">
                <sqbl:Maximum value="{max/text()}"/>
            </xsl:if>
        </sqbl:Number>
    </xsl:template>
    <xsl:template match="response[free/format/text()='text'] | response[free/format/text()='longtext']">
        <sqbl:Text>
            <xsl:if test="free/label">
                <sqbl:Prefix>
                    <sqbl:TextComponent xml:lang="en"><xsl:value-of select="free/label"/></sqbl:TextComponent>
                </sqbl:Prefix>
            </xsl:if>
        </sqbl:Text>
    </xsl:template>
    <xsl:template match="response[free/format/text()='date']">
        <sqbl:Text/>        
    </xsl:template>
    <xsl:template match="response[fixed]">
        <sqbl:CodeList>
            <sqbl:Codes>
                <xsl:apply-templates select="fixed/category"/>
            </sqbl:Codes>
        </sqbl:CodeList>
    </xsl:template>
    <xsl:template match="category">
        <sqbl:CodePair code="{value/text()}">
            <xsl:choose>
                <xsl:when test="contingentQuestion">
                    <xsl:attribute name="freetext">True</xsl:attribute>
                    <sqbl:TextComponent xml:lang="en">
                        <xsl:value-of select="label"/>
                        <xsl:text> </xsl:text>
                        <xsl:value-of select="contingentQuestion/text"/>
                    </sqbl:TextComponent>
                </xsl:when>
                <xsl:otherwise>
                    <sqbl:TextComponent xml:lang="en"><xsl:value-of select="label"/></sqbl:TextComponent>
                </xsl:otherwise>
            </xsl:choose>
        </sqbl:CodePair>
    </xsl:template>
    
    
    <xsl:template match="@*|node()" />
    <xsl:template match="@*|node()" mode="convertRichText">
        <xsl:value-of select="." />
    </xsl:template>
</xsl:stylesheet>
