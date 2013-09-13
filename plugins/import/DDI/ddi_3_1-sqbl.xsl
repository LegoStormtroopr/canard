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
    xmlns:g="ddi:group:3_1"
    xmlns:d="ddi:datacollection:3_1"
    xmlns:dce="ddi:dcelements:3_1"
    xmlns:c="ddi:conceptualcomponent:3_1"
    xmlns:xhtml="http://www.w3.org/1999/xhtml"
    xmlns:a="ddi:archive:3_1"
    xmlns:m1="ddi:physicaldataproduct/ncube/normal:3_1"
    xmlns:ddi="ddi:instance:3_1 http://www.ddialliance.org/sites/default/files/schema/ddi3.1/instance.xsd"
    xmlns:m2="ddi:physicaldataproduct/ncube/tabular:3_1"
    xmlns:l="ddi:logicalproduct:3_1"
    xmlns:m3="ddi:physicaldataproduct/ncube/inline:3_1"
    xmlns:pd="ddi:physicaldataproduct:3_1"
    xmlns:cm="ddi:comparative:3_1"
    xmlns:s="ddi:studyunit:3_1"
    xmlns:r="ddi:reusable:3_1"
    xmlns:pi="ddi:physicalinstance:3_1"
    xmlns:ds="ddi:dataset:3_1"
    xmlns:pr="ddi:profile:3_1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    exclude-result-prefixes="g d dce c xhtml a m1 ddi m2 l m3 pd cm s r pi ds pr xsl"
    version="1.0">
    
    <xsl:output method="xml" indent="yes"/>
    
    <xsl:param name="prefered-lang">en</xsl:param>
    
    <!-- If you dont specify any lang in your DDI, Klingon will be default. Qaplá!-->
    <xsl:param name="default-lang">tlh</xsl:param>
        
   <xsl:template match="*">
        <xsl:choose>
            <xsl:when test="count(//s:StudyUnit) > 0">
                <xsl:apply-templates select="//s:StudyUnit" mode="generateSQBLDoc"/>
            </xsl:when>
            <xsl:when test="count(//d:Instrument)">
                <xsl:apply-templates select="//d:Instrument" mode="generateSQBLDoc"/>
            </xsl:when>
        </xsl:choose>
    </xsl:template>    
        
    <xsl:template match="s:StudyUnit" mode="generateSQBLDoc">
        <sqbl:QuestionModule xsi:schemaLocation="sqbl:1 https://raw.github.com/LegoStormtroopr/sqbl-schema/master/Schemas/sqbl.xsd">
            <xsl:attribute name="name">id-<xsl:value-of select="substring(@id,0,29)"/></xsl:attribute>
            <sqbl:TextComponent>
                <sqbl:Title>
                    <xsl:choose>
                        <xsl:when test="r:Citation/r:Title[@xml:lang=$prefered-lang]">
                            <xsl:value-of select="r:Citation/r:Title[@xml:lang=$prefered-lang]/text()"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="r:Citation/r:Title[1]/text()"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </sqbl:Title>
                <sqbl:TargetRespondent></sqbl:TargetRespondent>
            </sqbl:TextComponent>
            <sqbl:ModuleLogic>
                <xsl:choose>
                    <xsl:when test="d:DataCollection/d:Instrument">
                        <xsl:apply-templates select="d:DataCollection/d:Instrument" />
                    </xsl:when>
                    <xsl:when test="d:DataCollection/d:ControlConstructScheme">
                        <xsl:apply-templates select="d:DataCollection/d:ControlConstructScheme" />
                    </xsl:when>
                    <xsl:when test="//d:ControlConstructScheme">
                        <xsl:apply-templates select="//d:ControlConstructScheme" />
                    </xsl:when>
                    <xsl:when test="d:DataCollection/d:QuestionScheme">
                        <xsl:apply-templates select="d:DataCollection/d:QuestionScheme" />
                    </xsl:when>
                </xsl:choose>
            </sqbl:ModuleLogic>
        </sqbl:QuestionModule>
    </xsl:template>

    <xsl:template match="d:Instrument" mode="generateSQBLDoc">
        <sqbl:QuestionModule xsi:schemaLocation="sqbl:1 https://raw.github.com/LegoStormtroopr/sqbl-schema/master/Schemas/sqbl.xsd">
            <xsl:attribute name="name">id-<xsl:value-of select="substring(@id,0,29)"/></xsl:attribute>
            <sqbl:TextComponent>
                <sqbl:Title>
                    <xsl:apply-templates select="d:InstrumentName/*" mode="convertRichText"/>
                </sqbl:Title>
                <sqbl:Purpose>
                    <xsl:apply-templates select="r:Description/*" mode="convertRichText"/>
                </sqbl:Purpose>
                <sqbl:TargetRespondent></sqbl:TargetRespondent>
            </sqbl:TextComponent>
            <sqbl:ModuleLogic>
                <xsl:apply-templates select="." />
            </sqbl:ModuleLogic>
        </sqbl:QuestionModule>
    </xsl:template>
    
    <xsl:template match="d:Instrument">
        <xsl:apply-templates select="d:ControlConstructReference"/>
    </xsl:template>
    
    <xsl:template match="d:ControlConstructScheme">
        <xsl:apply-templates select="d:QuestionConstruct | d:StatementItem"/>
    </xsl:template>
    
    <xsl:template match="d:QuestionConstruct">
        <xsl:variable name="qrId" select="d:QuestionReference/r:ID"/>
        <xsl:apply-templates select="//d:QuestionItem[@id = $qrId] | //d:MultipleQuestionItem[@id = $qrId]" />
    </xsl:template>
    
    <xsl:template match="d:Sequence">
        <xsl:apply-templates select="d:ControlConstructReference"/>
    </xsl:template>

    <!-- All these references act the same -->
    <xsl:template match="d:ControlConstructReference | d:ThenConstructReference | d:ElseConstructReference">
        <xsl:variable name="ccId" select="r:ID"/>
        <xsl:apply-templates select="//d:Sequence[@id = $ccId] | //d:QuestionConstruct[@id = $ccId] | //d:IfThenElse[@id = $ccId]" />
    </xsl:template>
    
    <xsl:template match="d:IfThenElse">
        <sqbl:ConditionalTree name="{@id}">
            <sqbl:SequenceGuide>
                <sqbl:Condition resultBranch="{d:ThenConstructReference/r:ID}">
                    <!-- For the time being generate a bogus, but 'valid' ValueOf -->
                    <sqbl:ValueOf question="{@id}" is="equal_to">N</sqbl:ValueOf>
                </sqbl:Condition>
            </sqbl:SequenceGuide>
            <xsl:apply-templates select="d:ThenConstructReference | d:ElseConstructReference" mode="makeBranch"/>
        </sqbl:ConditionalTree>
    </xsl:template>
    
    <xsl:template match="d:ThenConstructReference | d:ElseConstructReference" mode="makeBranch">
        <sqbl:Branch name="{r:ID/text()}">
            <sqbl:BranchLogic>
                <xsl:apply-templates select="."/>
            </sqbl:BranchLogic>
        </sqbl:Branch>
    </xsl:template>
    
    <xsl:template match="d:QuestionScheme">       
        <xsl:apply-templates select="d:QuestionItem | d:MultipleQuestionItem" />                  
    </xsl:template>

    <xsl:template match="d:QuestionItem">
        <sqbl:Question>        
            <xsl:attribute name="name">q<xsl:value-of select="substring(@id,0,30)"/></xsl:attribute>
            <xsl:for-each select="d:QuestionText">
                <sqbl:TextComponent>
                    <xsl:attribute name="xml:lang">
                        <xsl:choose>
                            <xsl:when test="d:LiteralText/ancestor-or-self::*[attribute::xml:lang][1]/@xml:lang">
                                <xsl:value-of select="d:LiteralText/ancestor-or-self::*[attribute::xml:lang][1]/@xml:lang"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="$default-lang"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:attribute>
                    <sqbl:QuestionText><xsl:value-of select="d:LiteralText/d:Text"/></sqbl:QuestionText>
                    <xsl:choose>
                        <xsl:when test="parent::d:QuestionIntent[@xml:lang = ./d:LiteralText/ancestor-or-self::*[attribute::xml:lang][1]/@xml:lang]">
                        </xsl:when>
                        <xsl:when test="parent::d:QuestionIntent">
                            <sqbl:QuestionIntent><xsl:value-of select="../d:QuestionIntent"/></sqbl:QuestionIntent>
                        </xsl:when>
                    </xsl:choose>
                </sqbl:TextComponent>
            </xsl:for-each>
            <sqbl:ResponseType>
                <xsl:apply-templates select="d:TextDomain | d:NumericDomain | d:CodeDomain | d:StructuredMixedResponseDomain/* | d:DateTimeDomain | d:CategoryDomain"/>
            </sqbl:ResponseType>
        </sqbl:Question>
    </xsl:template>
    
    <xsl:template match="d:TextDomain">
        <sqbl:Text>
            <xsl:if test="@maxLength">
                <sqbl:MaximumLength><xsl:value-of select="@maxLength"/></sqbl:MaximumLength>
            </xsl:if>
        </sqbl:Text>
    </xsl:template>

    <!-- TODO: Need to do this better -->
    <xsl:template match="d:DateTimeDomain">
        <sqbl:Text/>
    </xsl:template>
    
    <xsl:template match="d:NumericDomain">
        <sqbl:Number>
            <xsl:if test="@type='Integer'">
                <xsl:attribute name="interval">1</xsl:attribute>
            </xsl:if>
            <xsl:if test="r:NumberRange/r:Low">
                <sqbl:Minimum><xsl:value-of select="r:NumberRange/r:Low"/></sqbl:Minimum>
            </xsl:if>
            <xsl:if test="r:NumberRange/r:High">
                <sqbl:Maximum><xsl:value-of select="r:NumberRange/r:High"/></sqbl:Maximum>
            </xsl:if>            
            <xsl:for-each select="d:Label">
                <sqbl:Prefix>
                    <xsl:choose>
                        <xsl:when test="@xml:lang"><xsl:attribute name="xml:lang"><xsl:value-of select="@xml:lang"/></xsl:attribute></xsl:when>
                        <xsl:otherwise><xsl:attribute name="xml:lang"><xsl:value-of select="$default-lang"/></xsl:attribute></xsl:otherwise>
                    </xsl:choose>
                    <xsl:value-of select="."/>
                </sqbl:Prefix>
            </xsl:for-each>
        </sqbl:Number>
    </xsl:template>
    
    <xsl:template match="d:CategoryDomain">
        <xsl:variable name="catsId" select="r:CategorySchemeReference/r:ID"/>
        <xsl:comment><xsl:value-of select="$catsId"/></xsl:comment>
        <xsl:apply-templates select="//l:CategoryScheme[@id = $catsId]" />
    </xsl:template>
    
    <xsl:template match="l:CategoryScheme">
        <sqbl:CodeList>
            <sqbl:Codes>
                <xsl:for-each select="l:Category">
                   <sqbl:CodePair>
                       <xsl:attribute name="code"><xsl:value-of select="position()"/></xsl:attribute>
                       <xsl:apply-templates select="." />
                   </sqbl:CodePair>
               </xsl:for-each>
            </sqbl:Codes>
            <sqbl:MaximumSelections value="{count(l:Category)}"/>
        </sqbl:CodeList>
    </xsl:template>
    
    <xsl:template match="d:CodeDomain">
        <sqbl:CodeList>
            <xsl:variable name="qsId" select="r:CodeSchemeReference/r:ID"/>
            <xsl:apply-templates select="//l:CodeScheme[@id = $qsId]" />
        </sqbl:CodeList>        
    </xsl:template>
    
    <xsl:template match="d:MultipleQuestionItem">
        <sqbl:Statement>
            <xsl:attribute name="name"><xsl:value-of select="substring(@id,0,32)"/></xsl:attribute>
            <xsl:for-each select="d:QuestionText">
               <sqbl:TextComponent>
                   <xsl:attribute name="xml:lang">
                       <xsl:choose>
                           <xsl:when test="./ancestor-or-self::*[attribute::xml:lang][1]/@xml:lang">
                               <xsl:value-of select="d:LiteralText/ancestor-or-self::*[attribute::xml:lang][1]/@xml:lang"/>
                           </xsl:when>
                           <xsl:otherwise>
                               <xsl:value-of select="$default-lang"/>
                           </xsl:otherwise>
                       </xsl:choose>
                   </xsl:attribute>   
                   <sqbl:StatementText><xsl:value-of select="d:LiteralText/d:Text"/></sqbl:StatementText>
               </sqbl:TextComponent> 
            </xsl:for-each>
        </sqbl:Statement>
        <xsl:apply-templates select="d:SubQuestions/d:QuestionItem"/>
    </xsl:template>
    
    <xsl:template match="d:StatementItem">
        <sqbl:Statement>
            <xsl:attribute name="name"><xsl:value-of select="substring(@id,0,32)"/></xsl:attribute>
            <xsl:for-each select="d:DisplayText">
                <sqbl:TextComponent>
                    <xsl:attribute name="xml:lang">
                        <xsl:choose>
                            <xsl:when test="./ancestor-or-self::*[attribute::xml:lang][1]/@xml:lang">
                                <xsl:value-of select="d:LiteralText/ancestor-or-self::*[attribute::xml:lang][1]/@xml:lang"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="$default-lang"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:attribute>                    
                    <sqbl:StatementText><xsl:value-of select="d:LiteralText/d:Text"/></sqbl:StatementText>
                </sqbl:TextComponent>
            </xsl:for-each>
        </sqbl:Statement>
    </xsl:template>

    <xsl:template match="l:CodeScheme">
        <sqbl:Codes>
            <xsl:apply-templates select="l:Code"/>
        </sqbl:Codes>
    </xsl:template>
    
    <xsl:template match="l:Code">
        <sqbl:CodePair>
           <xsl:attribute name="code"><xsl:value-of select="l:Value"/></xsl:attribute>
           <xsl:variable name="cId" select="l:CategoryReference/r:ID"/>
           <xsl:apply-templates select="//l:Category[@id = $cId]" />
        </sqbl:CodePair>
    </xsl:template>
    
    <xsl:template match="l:Category">
        <xsl:for-each select="r:Label">
            <sqbl:TextComponent>
                <xsl:attribute name="xml:lang"><xsl:value-of select="ancestor-or-self::*[attribute::xml:lang][1]/@xml:lang"/></xsl:attribute>
                <xsl:value-of select="."/>
            </sqbl:TextComponent>
        </xsl:for-each>
    </xsl:template>
    
    <!-- We will need more ways to bring rich text across, but for now this will do. -->
    <xsl:template match="@*|node()" mode="convertRichText">
        <xsl:value-of select="."/>
    </xsl:template>
</xsl:stylesheet>