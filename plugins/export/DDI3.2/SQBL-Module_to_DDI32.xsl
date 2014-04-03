<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:exslt="http://exslt.org/common" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:fn="http://www.w3.org/2005/xpath-functions" xmlns:sqbl="sqbl:1"
	
	
		xmlns:ddi="ddi:instance:3_2" xmlns:a="ddi:archive:3_2" xmlns:c="ddi:conceptualcomponent:3_2"
		xmlns:cm="ddi:comparative:3_2" xmlns:d="ddi:datacollection:3_2" xmlns:g="ddi:group:3_2"
		xmlns:l="ddi:logicalproduct:3_2" xmlns:p="ddi:physicaldataproduct:3_2" xmlns:pi="ddi:physicalinstance:3_2"
		xmlns:pr="ddi:ddiprofile:3_2" xmlns:r="ddi:reusable:3_2" xmlns:s="ddi:studyunit:3_2"
		
		xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xhtml="http://www.w3.org/1999/xhtml"
			
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
	exclude-result-prefixes="exslt fn fo xsl" extension-element-prefixes="exslt">
	<xsl:output method="xml" />
	<xsl:param name="agency">com.kidstrythisathome.ddirepo.legostormtroopr</xsl:param>
	<xsl:param name="base_url">www.kidstrythisathome.com</xsl:param>
	<xsl:variable name="moduleName" select="/sqbl:QuestionModule/@name" />
	<xsl:template name="qualID">
		<xsl:param name="qualifier"/>
		<r:Agency><xsl:value-of select="$agency"/></r:Agency>
		<r:ID><xsl:value-of select="$moduleName"/><xsl:value-of select="$qualifier"/></r:ID>
		<r:Version>0.1</r:Version>		
	</xsl:template>
	<xsl:template name="makeID">
		<xsl:param name="id"/>
		<r:Agency><xsl:value-of select="$agency"/></r:Agency>
		<r:ID><xsl:value-of select="$id"/></r:ID>
		<r:Version>0.1</r:Version>		
	</xsl:template>
	<xsl:template match="/">
		<g:ResourcePackage isMaintainable="true"  versionDate="2012-09-18" scopeOfUniqueness="Maintainable" xsi:schemaLocation="ddi:instance:3_2 http://www.ddialliance.org/Specification/DDI-Lifecycle/3.2/XMLSchema/instance.xsd"> 
			<xsl:call-template name="qualID">
				<xsl:with-param name="qualifier">_ResourcePackage</xsl:with-param>
			</xsl:call-template>
					<d:DataCollection>
						<xsl:call-template name="qualID">
							<xsl:with-param name="qualifier">_DataCollection</xsl:with-param>
						</xsl:call-template>
						
						<d:QuestionScheme>
							<xsl:call-template name="qualID">
								<xsl:with-param name="qualifier">_QuestionScheme</xsl:with-param>
							</xsl:call-template>
							<xsl:apply-templates select="//sqbl:Question" mode="makeQuestionScheme" />
						</d:QuestionScheme>
						<d:ControlConstructScheme>
							<xsl:call-template name="qualID">
								<xsl:with-param name="qualifier">_QuestionConstructs</xsl:with-param>
							</xsl:call-template>
							<xsl:apply-templates select="//sqbl:Question" mode="makeQuestionConstructs" />
						</d:ControlConstructScheme>
						<d:ControlConstructScheme>
							<xsl:call-template name="qualID">
								<xsl:with-param name="qualifier">_ModuleLogic</xsl:with-param>
							</xsl:call-template>
							<xsl:apply-templates select="//sqbl:ModuleLogic" mode="makeLogicConstructs" />
						</d:ControlConstructScheme>
					</d:DataCollection>
					<l:LogicalProduct>
						<xsl:call-template name="qualID">
							<xsl:with-param name="qualifier">_LogicalProduct</xsl:with-param>
						</xsl:call-template>
						<xsl:apply-templates select="//sqbl:ResponseType/sqbl:CodeList" mode="makeCategorySchemes"/>
						<l:CodeListScheme>
							<xsl:call-template name="qualID">
								<xsl:with-param name="qualifier">_Codelists</xsl:with-param>
							</xsl:call-template>
							<xsl:apply-templates select="//sqbl:ResponseType/sqbl:CodeList" mode="makeCodeSchemes"/>
						</l:CodeListScheme>
					</l:LogicalProduct>
			</g:ResourcePackage>
		
	</xsl:template>
	<xsl:template match="*" mode="makeQuestionScheme" />
	<xsl:template match="sqbl:Question" mode="makeQuestionScheme">
		<d:QuestionItem ><xsl:call-template name="makeID">
				<xsl:with-param name="id"><xsl:value-of select="@name"/></xsl:with-param>
			</xsl:call-template>
			<xsl:apply-templates select="sqbl:TextComponent/sqbl:QuestionText" mode="makeQuestionScheme" />
			
			<xsl:if test="sqbl:TextComponent/sqbl:QuestionIntent">
				<d:QuestionIntent>
					<xsl:apply-templates select="sqbl:TextComponent/sqbl:QuestionIntent" mode="makeQuestionScheme" />
				</d:QuestionIntent>
			</xsl:if>
			<xsl:apply-templates select="sqbl:ResponseType" mode="makeQuestionScheme" />
		</d:QuestionItem>
	</xsl:template>
	<xsl:template match="sqbl:QuestionText" mode="makeQuestionScheme">
		<d:QuestionText audienceLanguage="{../@xml:lang}">
			<d:LiteralText>
				<d:Text>
					<xsl:value-of select="." />
				</d:Text>
			</d:LiteralText>
		</d:QuestionText>
	</xsl:template>
	<xsl:template match="sqbl:QuestionIntent" mode="makeQuestionScheme">
			<r:Content xml:lang="{../@xml:lang}">
			<xsl:value-of select="." />
			</r:Content>

	</xsl:template>
	<xsl:template match="sqbl:ResponseType" mode="makeQuestionScheme">
		<xsl:choose>
			<xsl:when test="count(*) > 1">
				<d:StructuredMixedResponseDomain>
					<xsl:for-each select="*">
					<d:ResponseDomainInMixed>
						<xsl:apply-templates select="." mode="makeQuestionScheme"/>
					</d:ResponseDomainInMixed>
					</xsl:for-each>
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
			<r:CodeListReference>
				<xsl:call-template name="makeID">
					<xsl:with-param name="id"><xsl:value-of select="ancestor::*[local-name()='Question'][1]/@name"/>_CodeList</xsl:with-param>
				</xsl:call-template>
				<r:TypeOfObject>CodeList</r:TypeOfObject>
			</r:CodeListReference>
		</d:CodeDomain>
	</xsl:template>
	<xsl:template match="sqbl:ResponseType/sqbl:Number" mode="makeQuestionScheme">
		<d:NumericDomain>
			<!-- xsl:if test="./sqbl:Step">
				Steps are no longer decimal, so we can't output them.
				<xsl:attribute name="interval"><xsl:value-of select="sqbl:Step/@value"/></xsl:attribute>
			</xsl:if -->
			<r:NumberRange>
			<xsl:if test="./sqbl:Minimum">
				<xsl:element name="r:Low"><xsl:value-of select="sqbl:Minimum/@value"/></xsl:element>
			</xsl:if>
			<xsl:if test="./sqbl:Maximum">
				<xsl:element name="r:High"><xsl:value-of select="sqbl:Maximum/@value"/></xsl:element>
			</xsl:if>
			</r:NumberRange>
			<xsl:apply-templates select="*/sqbl:TextComponent" mode="makeQuestionScheme"/>
		</d:NumericDomain>
	</xsl:template>
	<xsl:template match="sqbl:ResponseType//sqbl:TextComponent" mode="makeQuestionScheme">
		<r:Label>
			<r:Content xml:lang="{@xml:lang}"> 
			<xsl:value-of select="."/>
			</r:Content>
			<r:TypeOfLabel>x+sqbl/<xsl:value-of select="local-name(..)"></xsl:value-of></r:TypeOfLabel>
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
		<l:CategoryScheme>
			<xsl:call-template name="makeID">
				<xsl:with-param name="id"><xsl:value-of select="ancestor-or-self::*[local-name()='Question'][1]/@name"/>_CategoryScheme</xsl:with-param>
			</xsl:call-template>
			<xsl:apply-templates select="sqbl:Codes/sqbl:CodePair" mode="makeCategorySchemes"/>
		</l:CategoryScheme>
	</xsl:template>
	<xsl:template match="sqbl:CodePair" mode="makeCategorySchemes">
		<l:Category>
			<xsl:call-template name="makeID">
				<xsl:with-param name="id"><xsl:value-of select="ancestor-or-self::*[local-name()='Question'][1]/@name"/>_<xsl:value-of select="@code"/></xsl:with-param>
			</xsl:call-template>
			<xsl:apply-templates select="./sqbl:TextComponent" mode="makeCategorySchemes"/>
		</l:Category>
	</xsl:template>
	
	<xsl:template match="sqbl:CodePair/sqbl:TextComponent" mode="makeCategorySchemes">
		<r:Label><r:Content xml:lang="{@xml:lang}"><xsl:value-of select="."/></r:Content></r:Label>
	</xsl:template>
	
	<xsl:template match="sqbl:ResponseType/sqbl:CodeList" mode="makeCodeSchemes">
		<l:CodeList>
			<xsl:call-template name="makeID">
				<xsl:with-param name="id"><xsl:value-of select="ancestor-or-self::*[local-name()='Question'][1]/@name"/>_CodeList</xsl:with-param>
			</xsl:call-template>
			<xsl:apply-templates select="sqbl:Codes/sqbl:CodePair" mode="makeCodeSchemes"/>
		</l:CodeList>
	</xsl:template>
	
	<xsl:template match="sqbl:CodePair" mode="makeCodeSchemes">
		<l:Code>
			<xsl:call-template name="makeID">
				<xsl:with-param name="id"><xsl:value-of select="ancestor-or-self::*[local-name()='Question'][1]/@name"/>_Code<xsl:value-of select="@code"/></xsl:with-param>
			</xsl:call-template>
			<r:CategoryReference>
				<xsl:call-template name="makeID">
					<xsl:with-param name="id"><xsl:value-of select="ancestor-or-self::*[local-name()='Question'][1]/@name"/>_<xsl:value-of select="@code"/></xsl:with-param>
				</xsl:call-template>
				<r:TypeOfObject>Category</r:TypeOfObject>
			</r:CategoryReference>
			<r:Value><xsl:value-of select="@code"/></r:Value>
		</l:Code>
	</xsl:template>

	<xsl:template match="sqbl:Question" mode="makeQuestionConstructs">
		<d:QuestionConstruct>
			<xsl:call-template name="makeID">
				<xsl:with-param name="id"><xsl:value-of select="@name"/>_QC</xsl:with-param>
			</xsl:call-template>
			<r:QuestionReference>
				<xsl:call-template name="makeID">
					<xsl:with-param name="id"><xsl:value-of select="@name"/></xsl:with-param>
				</xsl:call-template>
				<r:TypeOfObject>QuestionItem</r:TypeOfObject>
			</r:QuestionReference>
		</d:QuestionConstruct>
	</xsl:template>

	<xsl:template match="sqbl:ModuleLogic" mode="makeLogicConstructs">
		<d:Sequence>
			<xsl:call-template name="makeID">
				<xsl:with-param name="id"><xsl:value-of select="$moduleName"/>_ModuleLogic</xsl:with-param>
			</xsl:call-template>
			<xsl:apply-templates select="*" mode="makeLogicConstructs_refs"/>
		</d:Sequence>
		<xsl:apply-templates select="*" mode="makeLogicConstructs"/>
	</xsl:template>

	<xsl:template match="*" mode="makeLogicConstructs_refs">
		<d:ControlConstructReference>
			<xsl:call-template name="makeID">
				<xsl:with-param name="id"><xsl:value-of select="@name"/></xsl:with-param>
			</xsl:call-template>
			<r:TypeOfObject>ControlConstructGroup</r:TypeOfObject>
		</d:ControlConstructReference>
	</xsl:template>
	
	<xsl:template match="sqbl:ConditionalTree" mode="makeLogicConstructs">
		<d:IfThenElse ><xsl:call-template name="makeID">
				<xsl:with-param name="id"><xsl:value-of select="@name"/></xsl:with-param>
			</xsl:call-template>
			<xsl:apply-templates select="sqbl:SequenceGuide/sqbl:Condition[1]" mode="makeLogicConstructs"/>
			<xsl:for-each select="sqbl:SequenceGuide/sqbl:Condition[position()>1]">
				<d:ElseIf>
					<xsl:apply-templates select="." mode="makeLogicConstructs"/>
				</d:ElseIf>	
			</xsl:for-each>
			<xsl:if test="sqbl:SequenceGuide/sqbl:Otherwise">
				<d:ElseConstructReference>
					<xsl:call-template name="makeID">
						<xsl:with-param name="id"><xsl:value-of select="sqbl:SequenceGuide/sqbl:Otherwise/@branch"/></xsl:with-param>
					</xsl:call-template>
					<r:TypeOfObject>ControlConstructGroup</r:TypeOfObject>
				</d:ElseConstructReference>
			</xsl:if>
		</d:IfThenElse>
		<xsl:apply-templates select="sqbl:Branch" mode="makeLogicConstructs"/>
	</xsl:template>
	<xsl:template match="sqbl:Condition" mode="makeLogicConstructs">
		<d:IfCondition>
			<r:Command>
				<r:ProgramLanguage>x+sqbl/conditionalTable</r:ProgramLanguage>
				<r:CommandContent>
				<xsl:text disable-output-escaping="yes">
	                    &lt;![CDATA[
	            </xsl:text>
				<xsl:apply-templates select="." mode="ident"/>
				<xsl:text disable-output-escaping="yes">
                 ]]&gt;
            	</xsl:text>
				</r:CommandContent>
			</r:Command>
		</d:IfCondition>
		<d:ThenConstructReference>
			<xsl:call-template name="makeID">
				<xsl:with-param name="id"><xsl:value-of select="@resultBranch"/></xsl:with-param>
			</xsl:call-template>
			<r:TypeOfObject>ControlConstructGroup</r:TypeOfObject>
		</d:ThenConstructReference>
	</xsl:template>
	<xsl:template match="sqbl:Branch" mode="makeLogicConstructs">
		<d:Sequence ><xsl:call-template name="makeID">
				<xsl:with-param name="id"><xsl:value-of select="@name"/></xsl:with-param>
			</xsl:call-template>
			<xsl:apply-templates select="sqbl:TextComponent/sqbl:Purpose" mode="makeLogicConstructs"/>
			<xsl:apply-templates select="sqbl:BranchLogic/*" mode="makeLogicConstructs_refs"/>
		</d:Sequence>
	</xsl:template>
	<xsl:template match="sqbl:Branch/sqbl:TextComponent/sqbl:Purpose" mode="makeLogicConstructs">
		<r:Description audienceLanguage="{@xml:lang}>">
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
