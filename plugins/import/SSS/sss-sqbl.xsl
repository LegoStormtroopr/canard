<?xml version="1.0" encoding="UTF-8"?>
<!--
    Document   : ddi_3_1-sbql.xsl
    Created on : den 2 juni 2013, 14:32
    Author     : Olof Olsson <borsna@gmail.com>
    License    : Public domain
    Extensions : *.xml, *.ddi3
    Description:
        Transform DDI 3.1 Questionaires to SQBL
    
    TODO:
        cover sequences
-->

<xsl:stylesheet 
    xsi:schemaLocation="sqbl:1 https://raw.github.com/LegoStormtroopr/sqbl-schema/master/Schemas/sqbl.xsd"
    xmlns:sqbl="sqbl:1"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:xhtml="http://www.w3.org/1999/xhtml"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    exclude-result-prefixes="xhtml xsl"
    version="1.0">
    
    <xsl:output method="xml" indent="yes"/>
    
    <xsl:param name="prefered-lang">en</xsl:param>
       
    <xsl:template match="/sss">
      <xsl:apply-templates select="//survey"/>
    </xsl:template>
           
    <xsl:template match="survey">
        <sqbl:QuestionModule
            version="1"
            name="{name/text()}"      
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="sqbl:1 https://raw.github.com/LegoStormtroopr/sqbl-schema/master/Schemas/sqbl.xsd"
            >
            <sqbl:TextComponents>
                <sqbl:TextComponent xml:lang="en">
                    <sqbl:LongName><xsl:value-of select="title"/></sqbl:LongName>
                    <sqbl:Title><xsl:value-of select="title"/></sqbl:Title>
                </sqbl:TextComponent>
            </sqbl:TextComponents>
            <sqbl:ModuleLogic>
                <xsl:apply-templates select="record/variable"/>
            </sqbl:ModuleLogic>       
        </sqbl:QuestionModule>
    </xsl:template>
   
    <xsl:template match="variable[not(@use='weight')]">
        <sqbl:Question name="{name/text()}">
            <sqbl:TextComponent xml:lang="en">
                <sqbl:QuestionText>
                    <xsl:value-of select="label/text[@mode='interview']/text()"/>
                </sqbl:QuestionText>
                <sqbl:QuestionIntent>
                    <xsl:value-of select="label/text()"/>
                    <xsl:value-of select="label/text[@mode='analysis']/text()"/>
                </sqbl:QuestionIntent>
            </sqbl:TextComponent>
            <sqbl:ResponseType>
                <xsl:apply-templates select="values"/>
                <xsl:if test="not(values)">
                    <sqbl:Text/>
                </xsl:if>
            </sqbl:ResponseType>
        </sqbl:Question>
    </xsl:template>
    
    <xsl:template match="values[../@type='logical']">
        <sqbl:Boolean/>
    </xsl:template>
    <xsl:template match="values[../@type='quantity']">
        <sqbl:Number>
            
        </sqbl:Number>
    </xsl:template>
   
    <xsl:template match="values[../@type='single'] | values[../@type='multiple']">
        <sqbl:CodeList>
            <sqbl:Codes>
                <xsl:apply-templates select="value"/>
            </sqbl:Codes>
            <xsl:choose>
                <xsl:when test="../@type='single'">
                    <sqbl:MaximumSelections value="1"/>
                </xsl:when>
                <xsl:when test="spread">
                    <sqbl:MaximumSelections value="spread/@subfields"/>
                </xsl:when>
                <xsl:when test="../@type='multiple'">
                    <sqbl:MaximumSelections value="#all"/>
                </xsl:when>
            </xsl:choose>
        </sqbl:CodeList>
    </xsl:template>
    <xsl:template match="value">
        <sqbl:CodePair code="@code">
            <sqbl:TextComponent xml:lang="en"><xsl:value-of select="."/></sqbl:TextComponent>
        </sqbl:CodePair>
    </xsl:template>
    
    <xsl:template match="values[../@type='character']">
        <sqbl:Text/>
    </xsl:template>
    
    <xsl:template match="values">
        <sqbl:Text/>
    </xsl:template>
        
    <xsl:template match="@*|node()" />
        
    <xsl:template match="@*|node()" mode="convertRichText">
        <xsl:value-of select="."/>
    </xsl:template>
</xsl:stylesheet>