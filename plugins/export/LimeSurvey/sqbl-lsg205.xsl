<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:exslt="http://exslt.org/common" 
	xmlns:sqbl="sqbl:1"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
	xmlns:skip="http://legostormtoopr/skips"
	exclude-result-prefixes="sqbl xsl xsi skip">
	<xsl:import href="../SQBL_to_Skips.xsl" />
	<xsl:output method="xml" />
					
	<xsl:param name="agency">com.kidstrythisathome.ddirepo.legostormtroopr</xsl:param>
	<xsl:param name="base_url">www.kidstrythisathome.com</xsl:param>
	<xsl:variable name="moduleName" select="/sqbl:QuestionModule/@name" />
	<xsl:param name="lang" select="'en'" />

	<xsl:variable name="skips">
		<xsl:call-template name="makeSkips">
			<xsl:with-param name="doc" select="//sqbl:ModuleLogic" />
		</xsl:call-template>
	</xsl:variable>

	<xsl:template match="/">
		<xsl:apply-templates select="sqbl:QuestionModule" ></xsl:apply-templates>
	</xsl:template>
	<xsl:template match="sqbl:QuestionModule">
		<document xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="1">
			<LimeSurveyDocType>Group</LimeSurveyDocType>
			<DBVersion>177</DBVersion>
			<languages><language><xsl:value-of select="$lang"/></language></languages>
			<groups>
				<fields>
					<fieldname>gid</fieldname>
					<fieldname>sid</fieldname>
					<fieldname>group_name</fieldname>
					<fieldname>group_order</fieldname>
					<fieldname>description</fieldname>
					<fieldname>language</fieldname>
					<fieldname>randomization_group</fieldname>
					<fieldname>grelevance</fieldname>
				</fields>
				<rows>
					<row>
						<gid>40</gid>
						<sid>641191</sid>
						<group_name><xsl:value-of select="sqbl:TextComponents/sqbl:TextComponent[@xml:lang=$lang]/sqbl:Title"/></group_name>
						<group_order>37</group_order>
						<description><xsl:apply-templates select="sqbl:TextComponents/sqbl:TextComponent[@xml:lang=$lang]/sqbl:LongName" /></description>
						<language>en</language>
						<randomization_group/>
						<grelevance/>
					</row>
				</rows>
			</groups>
			<questions>
				<fields>
					<fieldname>qid</fieldname>
					<fieldname>parent_qid</fieldname>
					<fieldname>sid</fieldname>
					<fieldname>gid</fieldname>
					<fieldname>type</fieldname>
					<fieldname>title</fieldname>
					<fieldname>question</fieldname>
					<fieldname>preg</fieldname>
					<fieldname>help</fieldname>
					<fieldname>other</fieldname>
					<fieldname>mandatory</fieldname>
					<fieldname>question_order</fieldname>
					<fieldname>language</fieldname>
					<fieldname>scale_id</fieldname>
					<fieldname>same_default</fieldname>
					<fieldname>relevance</fieldname>
				</fields>
				<rows>
					<xsl:apply-templates select="//sqbl:Question"/>
				</rows>
			</questions>			
		</document>
	</xsl:template>
	<xsl:template match="sqbl:Question">
		<row>
			<qid><xsl:value-of select="@name" /></qid>
			<parent_qid>0</parent_qid>
			<sid>641191</sid>
			<gid>40</gid>
			<type>
				<xsl:if test="count(./sqbl:ResponseType) = 1">
					<xsl:choose>
						<xsl:when test="./sqbl:ResponseType/sqbl:Boolean"><xsl:text>Y</xsl:text></xsl:when>
						<xsl:when test="./sqbl:ResponseType/sqbl:Text/@displayType = 'short'"><xsl:text>S</xsl:text></xsl:when>
						<xsl:when test="./sqbl:ResponseType/sqbl:Text/@displayType = 'medium'"><xsl:text>T</xsl:text></xsl:when>
						<xsl:when test="./sqbl:ResponseType/sqbl:Text/@displayType = 'long'"><xsl:text>U</xsl:text></xsl:when>
						<xsl:when test="./sqbl:ResponseType/sqbl:Number"><xsl:text>N</xsl:text></xsl:when>
						<xsl:otherwise><xsl:text>S</xsl:text></xsl:otherwise>
					</xsl:choose>
				</xsl:if>
			</type>
			<title><xsl:value-of select="translate(@name,'-_','')" /></title>
			<question><xsl:apply-templates select="sqbl:TextComponent[@xml:lang=$lang]/sqbl:QuestionText" /></question>
			<preg/>
			<help><xsl:apply-templates select="sqbl:TextComponent[@xml:lang=$lang]/sqbl:QuestionIntent" /></help>
			<other>N</other>
			<mandatory>
				<xsl:choose>
					<xsl:when test="./sqbl:ResponseType/@canRefuse"><xsl:text>N</xsl:text></xsl:when>
					<xsl:otherwise><xsl:text>N</xsl:text></xsl:otherwise>
				</xsl:choose>
			</mandatory>
			<question_order><xsl:value-of select="position()" /></question_order>
			<language><xsl:value-of select="$lang"/></language>
			<scale_id>0</scale_id>
			<same_default>0</same_default>
			<relevance>1</relevance>
		</row>
	</xsl:template>
	<xsl:template match="sqbl:SubQuestion">
		<xsl:variable name="parentQuestion" select="../../@name"/>
		<subQuestion varName="{$parentQuestion}_sub_{position()}">
			<text>
				<xsl:value-of select="sqbl:TextComponent[@xml:lang=$lang]" />
			</text>
		</subQuestion>
	</xsl:template>
		
	<xsl:template match="sqbl:QuestionText">
		<xsl:value-of select="." />
	</xsl:template>
	<xsl:template match="sqbl:QuestionIntent">
		<xsl:value-of select="." />
	</xsl:template>
	<xsl:template match="sqbl:ResponseType/*" mode="makeResponse">
		<xsl:variable name="parentQuestion" select="../../@name"/>
		<response varName="{$parentQuestion}_resp_{position()}">
			<xsl:apply-templates select="self::*" mode="makeResponseSubtype" />
		</response>
	</xsl:template>

	<xsl:template match="sqbl:ResponseType/sqbl:Number|sqbl:ResponseType/sqbl:Text" mode="makeResponseSubtype">
		<free>
			<format>integer</format>
			<length>
				<xsl:choose>
					<xsl:when test="sqbl:Maximum/@value"><xsl:value-of select="string-length(sqbl:Maximum/@value)"/></xsl:when>
					<xsl:when test="self::sqbl:Text/@displayType = 'medium'">256</xsl:when>
					<xsl:when test="self::sqbl:Text/@displayType = 'long'">512</xsl:when>
					<xsl:otherwise>128</xsl:otherwise>
				</xsl:choose>
			</length>			
			<label>
				<xsl:if test="sqbl:Hint">
					Hint: <xsl:value-of select="sqbl:Hint"/>
				</xsl:if>
				<xsl:if test="sqbl:Prefix">
					Prefix: <xsl:value-of select="sqbl:Prefix"/>
				</xsl:if>
				<xsl:if test="sqbl:Suffix">
					Suffix: <xsl:value-of select="sqbl:Suffix"/>
				</xsl:if>
			</label>
			<min><xsl:value-of select="sqbl:Minimum/@value"/></min>
			<max><xsl:value-of select="sqbl:Maximum/@value"/></max>
		</free>
	</xsl:template>
	<xsl:template match="sqbl:ResponseType/sqbl:Text" mode="makeResponseSubtype">
		<free>
			<format>
				<xsl:choose>
					<xsl:when test="self::sqbl:Text/@displayType = 'medium'">longtext</xsl:when>
					<xsl:when test="self::sqbl:Text/@displayType = 'long'">longtext</xsl:when>
					<xsl:otherwise>text</xsl:otherwise>
				</xsl:choose>
			</format>
			<length>
				<xsl:choose>
					<xsl:when test="sqbl:MaximumLength/@value"><xsl:value-of select="sqbl:MaximumLength/@value"/></xsl:when>
					<xsl:when test="self::sqbl:Text/@displayType = 'medium'">256</xsl:when>
					<xsl:when test="self::sqbl:Text/@displayType = 'long'">512</xsl:when>
					<xsl:otherwise>128</xsl:otherwise>
				</xsl:choose>
			</length>
			<xsl:if test="sqbl:Hint">
				<label><xsl:value-of select="sqbl:Hint"/></label>
			</xsl:if>			
		</free>
	</xsl:template>
	
	<xsl:template match="sqbl:ResponseType/sqbl:Boolean" mode="makeResponseSubtype">
	</xsl:template>
	<xsl:template match="sqbl:ResponseType/sqbl:CodeList" mode="makeResponseSubtype">
		<fixed>
			<xsl:apply-templates select="sqbl:Codes/sqbl:CodePair"></xsl:apply-templates>
		</fixed>
	</xsl:template>
	<xsl:template match="sqbl:CodePair">
		<category>
			<label><xsl:value-of select="sqbl:TextComponent[@xml:lang=$lang]" /></label>
			<value><xsl:value-of select="@code" /></value>
			<xsl:if test="@freeText">
				<contingentQuestion varName="{ancestor::sqbl:Question/@name}_contingent_{@code}">
					<format>text</format>
					<text></text>
					<length>128</length>
				</contingentQuestion>
			</xsl:if>
			<xsl:variable name="name" select="ancestor::sqbl:Question/@name"/>
			<xsl:if test="count(exslt:node-set($skips)/skip:skips2/skip:link[@from=$name]) > 1">
				<xsl:variable name="value" select="@code"/>
				<xsl:choose>
					<xsl:when test="exslt:node-set($skips)/skip:skips2/skip:link[@from = $name]/skip:condition[@val = $value]">
						<xsl:variable name="to"><xsl:value-of select="exslt:node-set($skips)/skip:skips2/skip:link[@from = $name]/skip:condition[@val = $value]/../@to"/></xsl:variable>
						<skipTo><xsl:value-of select="$to"/>_resp_1</skipTo>
					</xsl:when>
					<xsl:when test="exslt:node-set($skips)/skip:skips2/skip:link[@from = $name and @condition = 'otherwise']">
						<xsl:variable name="to">
							<xsl:value-of select="exslt:node-set($skips)/skip:skips2/skip:link[@from = $name and @condition = 'otherwise'][1]/@to"/>
						</xsl:variable>
						<skipTo><xsl:value-of select="$to"/>_resp_1</skipTo>
					</xsl:when>
				</xsl:choose>
			</xsl:if>
							
		</category>
	</xsl:template>
		
	<xsl:template match="*"/>
	
	<xsl:template match="@*|node()" mode="ident">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()" mode="ident"/>
		</xsl:copy>
	</xsl:template>

</xsl:stylesheet>
