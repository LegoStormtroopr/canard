<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:sqbl="sqbl:1"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
	exclude-result-prefixes="sqbl xsl xsi">
	<xsl:output method="xml" />
	<xsl:param name="agency">com.kidstrythisathome.ddirepo.legostormtroopr</xsl:param>
	<xsl:param name="base_url">www.kidstrythisathome.com</xsl:param>
	<xsl:variable name="moduleName" select="/sqbl:QuestionModule/@name" />
	<xsl:template match="/">
		<xsl:text disable-output-escaping="yes">
			&lt;!DOCTYPE sss PUBLIC "-//triple-s//DTD Survey Interchange v2.0//EN"
                     "http://www.triple-s.org/dtd/sss_v20.dtd"&gt;
		</xsl:text>
		<sss version="2.0" modes="interview analysis">
			<date></date>
			<time></time>
			<origin>SQBL Output</origin>
			<user>Canard</user>
			<survey>
				<record ident="V">
					<xsl:apply-templates select="//sqbl:Question"/>
				</record>
			</survey>
		</sss>	
	
	</xsl:template>
	<xsl:template match="sqbl:Question">
		<variable ident="{position()}">
			<xsl:attribute name="type">
			<xsl:choose>
				<xsl:when test="count(sqbl:ResponseType)>1"></xsl:when>
				<xsl:when test="//sqbl:Number">quantity</xsl:when>
				<xsl:when test="//sqbl:Codelist[sqbl:MinimumSelections/@value >0]">multiple</xsl:when>
				<xsl:when test="//sqbl:Codelist[sqbl:MaximumSelections/@value >0]">multiple</xsl:when>
				<xsl:when test="//sqbl:Codelist[sqbl:MaximumSelections/@value >'#all']">multiple</xsl:when>
				<xsl:when test="//sqbl:CodeList">single</xsl:when>
				<xsl:when test="//sqbl:Boolean">logical</xsl:when>
				<xsl:when test="//sqbl:Text">character</xsl:when>
			</xsl:choose>
			</xsl:attribute>
			<name><xsl:value-of select="@name"></xsl:value-of></name>
			<label>
				<xsl:apply-templates select="sqbl:TextComponent/sqbl:QuestionText" />
				<xsl:apply-templates select="sqbl:TextComponent/sqbl:QuestionIntent" />
			</label>
			<position start="{position()}"/>
			<xsl:apply-templates select="sqbl:ResponseType" />
		</variable>
	</xsl:template>
	<xsl:template match="sqbl:QuestionText">
		<text mode="interview" xml:lang="{../@xml:lang}">
			<xsl:value-of select="." />
		</text>
	</xsl:template>
	<xsl:template match="sqbl:QuestionIntent">
		<text mode="analysis" xml:lang="{../@xml:lang}">
			<xsl:value-of select="." />
		</text>
	</xsl:template>
	<xsl:template match="sqbl:ResponseType">
		<!-- TODO: Include <values> -->
	</xsl:template>

	<xsl:template match="*"/>

	<xsl:template match="@*|node()" mode="ident">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()" mode="ident"/>
		</xsl:copy>
	</xsl:template>

</xsl:stylesheet>
