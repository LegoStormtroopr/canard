<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:exslt="http://exslt.org/common" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:fn="http://www.w3.org/2005/xpath-functions" xmlns:sqbl="sqbl:1" xmlns:ddi="ddi:instance:3_1"
	xmlns:a="ddi:archive:3_1" xmlns:r="ddi:reusable:3_1" xmlns:xhtml="http://www.w3.org/1999/xhtml"
	xmlns:d="ddi:datacollection:3_1" xmlns:l="ddi:logicalproduct:3_1" xmlns:c="ddi:conceptualcomponent:3_1"
	xmlns:ds="ddi:dataset:3_1" xmlns:s="ddi:studyunit:3_1" xmlns:g="ddi:group:3_1"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
	exclude-result-prefixes="exslt fn fo xsl" extension-element-prefixes="exslt">
	<xsl:output method="xml" />
	<xsl:param name="agency">com.kidstrythisathome.ddirepo.legostormtroopr</xsl:param>
	<xsl:param name="base_url">www.kidstrythisathome.com</xsl:param>
	<xsl:variable name="moduleName" select="/sqbl:QuestionModule/@name" />
	<xsl:template match="/">
		<ddi:DDIInstance id="x0" version="0.0.1" agency="com.kidstrythisathome.ddirepo.legostormtroopr">
			<g:ResourcePackage id="x1">
				<g:Purpose id="x2">
					<r:Content />
				</g:Purpose>
				<g:DataCollection>
					<d:DataCollection id="{$moduleName}_DataCollection">
						<d:QuestionScheme id="{$moduleName}_QuestionScheme">
							<xsl:apply-templates select="//sqbl:Question" mode="makeQuestionScheme" />
						</d:QuestionScheme>
						<d:ControlConstructScheme id="{$moduleName}_QuestionConstructs">
							<xsl:apply-templates select="//sqbl:Question" mode="makeQuestionConstructs" />
						</d:ControlConstructScheme>
						<d:ControlConstructScheme id="{$moduleName}_ModuleLogic">
							<xsl:apply-templates select="//sqbl:ModuleLogic" mode="makeLogicConstructs" />
						</d:ControlConstructScheme>
					</d:DataCollection>
				</g:DataCollection>
				<g:LogicalProduct>
					<l:LogicalProduct id="{$moduleName}_LogicalProduct">
						<xsl:apply-templates select="//sqbl:ResponseType/sqbl:CodeList" mode="makeCategorySchemes"/>
						<xsl:apply-templates select="//sqbl:ResponseType/sqbl:CodeList" mode="makeCodeSchemes"/>
					</l:LogicalProduct>
				</g:LogicalProduct>
			</g:ResourcePackage>
		</ddi:DDIInstance>
	</xsl:template>
	<xsl:template match="*" mode="makeQuestionScheme" />
	<xsl:template match="sqbl:Question" mode="makeQuestionScheme">
		<d:QuestionItem id="{@name}" objectSource="{$base_url}#{@name}">
			<xsl:apply-templates select="sqbl:TextComponent/sqbl:QuestionText" mode="makeQuestionScheme" />
			<xsl:apply-templates select="sqbl:TextComponent/sqbl:QuestionIntent" mode="makeQuestionScheme" />
			<xsl:apply-templates select="sqbl:ResponseType" mode="makeQuestionScheme" />
		</d:QuestionItem>
	</xsl:template>
	<xsl:template match="sqbl:QuestionText" mode="makeQuestionScheme">
		<d:QuestionText xml:lang="{../@xml:lang}">
			<d:LiteralText>
				<d:Text>
					<xsl:value-of select="." />
				</d:Text>
			</d:LiteralText>
		</d:QuestionText>
	</xsl:template>
	<xsl:template match="sqbl:QuestionIntent" mode="makeQuestionScheme">
		<d:QuestionIntent xml:lang="{../@xml:lang}">
			<xsl:value-of select="." />
		</d:QuestionIntent>
	</xsl:template>
	<xsl:template match="sqbl:ResponseType" mode="makeQuestionScheme">
		<xsl:choose>
			<xsl:when test="count(*) > 1">
				<d:StructuredMixedResponseDomain>
					<xsl:apply-templates select="*" mode="makeQuestionScheme"/>
				</d:StructuredMixedResponseDomain>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="*" mode="makeQuestionScheme"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="sqbl:ResponseType/*" mode="makeQuestionScheme">
		<d:TextDomain />
	</xsl:template>

	<xsl:template match="sqbl:ResponseType/sqbl:CodeList" mode="makeQuestionScheme">
		<d:CodeDomain>
			<r:CodeSchemeReference>
				<r:ID><xsl:value-of select="ancestor::*[local-name()='Question'][1]/@name"/>_CodeList</r:ID>
			</r:CodeSchemeReference>
		</d:CodeDomain>
	</xsl:template>
	<xsl:template match="sqbl:ResponseType/sqbl:Number" mode="makeQuestionScheme">
		<d:NumericDomain type="Decimal">
			<xsl:if test="./sqbl:Minimum">
				<xsl:attribute name="startValue" select="sqbl:Minimum/@value"/>
			</xsl:if>
			<xsl:if test="./sqbl:Maximum">
				<xsl:attribute name="endValue" select="sqbl:Maximum/@value"/>
			</xsl:if>
			<xsl:if test="./sqbl:Step">
				<xsl:attribute name="interval" select="sqbl:Step/@value"/>
			</xsl:if>
			<!-- Numbers use a wierd Label thats not r:Label, so we'll skip this 
				<xsl:apply-templates select="*/sqbl:TextComponent" mode="makeQuestionScheme"/>
			-->
		</d:NumericDomain>
	</xsl:template>
	<xsl:template match="sqbl:ResponseType//sqbl:TextComponent" mode="makeQuestionScheme">
		<r:Label xml:lang="{@xml:lang}" type="x+sqbl/{local-name(..)}">
			<xsl:value-of select="."/>
		</r:Label>
	</xsl:template>	
	
	<xsl:template match="sqbl:ResponseType/sqbl:Text" mode="makeQuestionScheme">
		<d:TextDomain>
			<xsl:if test="./sqbl:MinimumLength">
				<xsl:attribute name="minLength" select="sqbl:MinimumLength/@value"/>
			</xsl:if>
			<xsl:if test="./sqbl:MaximumLength">
				<xsl:attribute name="maxLength" select="sqbl:MaximumLength/@value"/>
			</xsl:if>
			<xsl:apply-templates select="*/sqbl:TextComponent" mode="makeQuestionScheme"/>
		</d:TextDomain>
	</xsl:template>

	<xsl:template match="sqbl:ResponseType/sqbl:CodeList" mode="makeCategorySchemes">
		<l:CategoryScheme id="{ancestor-or-self::*[local-name()='Question'][1]/@name}_CategoryScheme">
			<xsl:apply-templates select="sqbl:Codes/sqbl:CodePair" mode="makeCategorySchemes"/>
		</l:CategoryScheme>
	</xsl:template>
	<xsl:template match="sqbl:CodePair" mode="makeCategorySchemes">
		<l:Category id="{ancestor::*[local-name()='Question'][1]/@name}_{@code}">
			<xsl:apply-templates select="./sqbl:TextComponent" mode="makeCategorySchemes"/>
		</l:Category>
	</xsl:template>
	
	<xsl:template match="sqbl:CodePair/sqbl:TextComponent" mode="makeCategorySchemes">
		<r:Label xml:lang="{@xml:lang}"><xsl:value-of select="."></xsl:value-of></r:Label>
	</xsl:template>
	
	<xsl:template match="sqbl:ResponseType/sqbl:CodeList" mode="makeCodeSchemes">
		<l:CodeScheme id="{../../@name}_CodeList">
			<xsl:apply-templates select="sqbl:Codes/sqbl:CodePair" mode="makeCodeSchemes"/>
		</l:CodeScheme>
	</xsl:template>
	
	<xsl:template match="sqbl:CodePair" mode="makeCodeSchemes">
		<l:Code>
			<l:CategoryReference>
				<r:ID><xsl:value-of select="ancestor-or-self::*[local-name()='Question'][1]/@name"/>_<xsl:value-of select="@code"/></r:ID>
			</l:CategoryReference>
			<l:Value><xsl:value-of select="@code"/></l:Value>
		</l:Code>
	</xsl:template>

	<xsl:template match="sqbl:Question" mode="makeQuestionConstructs">
		<d:QuestionConstruct id="{@name}_QC">
			<d:QuestionReference>
				<r:ID><xsl:value-of select="@name"/></r:ID>
			</d:QuestionReference>
		</d:QuestionConstruct>
	</xsl:template>

	<xsl:template match="sqbl:ModuleLogic" mode="makeLogicConstructs">
		<d:Sequence id="{$moduleName}_ModuleLogic">
			<xsl:apply-templates select="*" mode="makeLogicConstructs_refs"/>
		</d:Sequence>
		<xsl:apply-templates select="*" mode="makeLogicConstructs"/>
	</xsl:template>

	<xsl:template match="*" mode="makeLogicConstructs_refs">
		<d:ControlConstructReference>
			<r:ID><xsl:value-of select="@name"/></r:ID>			
		</d:ControlConstructReference>
	</xsl:template>
	
	<xsl:template match="sqbl:ConditionalTree" mode="makeLogicConstructs">
		<d:IfThenElse id="@name">
			<xsl:apply-templates select="sqbl:SequenceGuide/sqbl:Condition[1]" mode="makeLogicConstructs"/>
			<xsl:for-each select="sqbl:SequenceGuide/sqbl:Condition[position()>1]">
				<d:ElseIf>
					<xsl:apply-templates select="." mode="makeLogicConstructs"/>
				</d:ElseIf>	
			</xsl:for-each>
			<xsl:if test="sqbl:SequenceGuide/sqbl:Otherwise">
				<d:ElseConstructReference>
					<r:ID><xsl:value-of select="sqbl:SequenceGuide/sqbl:Otherwise/@branch"></xsl:value-of></r:ID>
				</d:ElseConstructReference>
			</xsl:if>
		</d:IfThenElse>
		<xsl:apply-templates select="sqbl:Branch" mode="makeLogicConstructs"/>
	</xsl:template>
	<xsl:template match="sqbl:Condition" mode="makeLogicConstructs">
		<d:IfCondition>
			<r:Code programmingLanguage="x+sqbl/conditionalTable">
				<xsl:text disable-output-escaping="yes">
	                    &lt;![CDATA[
	            </xsl:text>
				<xsl:apply-templates select="." mode="ident"/>
				<xsl:text disable-output-escaping="yes">
                 ]]&gt;
            	</xsl:text>
			</r:Code>
		</d:IfCondition>
		<d:ThenConstructReference>
			<r:ID><xsl:value-of select="@resultBranch"/></r:ID>
		</d:ThenConstructReference>
	</xsl:template>
	<xsl:template match="sqbl:Branch" mode="makeLogicConstructs">
		<d:Sequence id="{@name}">
			<xsl:apply-templates select="sqbl:TextComponent/sqbl:Purpose" mode="makeLogicConstructs"/>
			<xsl:apply-templates select="sqbl:BranchLogic/*" mode="makeLogicConstructs_refs"/>
		</d:Sequence>
	</xsl:template>
	<xsl:template match="sqbl:Branch/sqbl:TextComponent/sqbl:Purpose" mode="makeLogicConstructs">
		<r:Description xml:lang="{@xml:lang}>">
			<xsl:value-of select="."/>
		</r:Description>
	</xsl:template>
	<xsl:template match="*" mode="makeLogicConstructs"/>

	<xsl:template match="@*|node()" mode="ident">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()" mode="ident"/>
		</xsl:copy>
	</xsl:template>

</xsl:stylesheet>
