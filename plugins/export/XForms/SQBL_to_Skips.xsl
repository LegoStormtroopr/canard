<?xml version="1.0" encoding="UTF-8"?>
<!-- edited with XMLSpy v2011 rel. 3 (http://www.altova.com) by .PCSoft (Australian Bureau of Statistics) -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:sqbl="sqbl:1"
	xmlns:skip="http://legostormtoopr/skips" xmlns:exslt="http://exslt.org/common">
	<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />
	<!-- The main template of this file is this section which begins the transformation
		of the hierarchical ResponseML into a skip based graph.
		 This graph then assists with the creation of the 'Go To' isntructions seen on web and paper forms.
	-->
	
	<xsl:template match="/">
		<x>
			<xsl:call-template name="makeSkips">
				<xsl:with-param name="doc" select="//sqbl:ModuleLogic"></xsl:with-param>
			</xsl:call-template>
		</x>
	</xsl:template>
	
	<xsl:template name="makeSkips">
		<xsl:param name="doc" />
		<xsl:variable name="seqGuide">
			<!--
				Now we make the first pass, and link things in the hierarchy, to the next object.
				Either their next sibling or their closest 'uncle' - i.e. the first sibling of ancestor.
				We convert conditional constructs to sequence guides.
				
				TODO: Loops (YOLO)
			-->
			<skip:skips>
				<xsl:apply-templates select="exslt:node-set($doc)/*" mode="toSequenceGuides" />
			</skip:skips>
		</xsl:variable>
		<xsl:variable name="seqGuide2">
			<skip:skips2>
				<xsl:apply-templates select="exslt:node-set($seqGuide)/skip:skips/*[1]" mode="removeSequenceGuides" />
			</skip:skips2>
		</xsl:variable>
		<xsl:copy-of select="$seqGuide" />
		<xsl:copy-of select="$seqGuide2" />
	</xsl:template>
	
	<xsl:template match="skip:link" mode="removeSequenceGuides">
		<xsl:variable name="from" select="@from" />
		<xsl:variable name="to" select="@to" />
		<xsl:variable name="next" select="following-sibling::*[1]" />
		<xsl:choose>
			<!--
				Now we try to remove sequence guides, if possible.
				At present this is met by the condition -
				   IF a link X is immediately followed by a sequenceGuide Y,
				      AND X is a path to Y,
				      AND X is the only path to the sequence guide
				      AND all of Ys conditions only depend on X,
				   THEN replace Y with the required number of links,
				   OTHERWISE keep X and Y as they are.
				We do this recursively, because we may have to jump things.
			-->
			<xsl:when
				test="local-name($next) = 'sequenceGuide' 
				and	$next/@from = $to
				and	count(//*[@to=$to]) = 1
				and	count($next//skip:condition) = count($next//skip:condition[@question=$from])
				">
				<xsl:for-each select="$next/skip:link">
					<xsl:element name="skip:link">
						<xsl:attribute name="from">
							<xsl:value-of select="$from" />
						</xsl:attribute>
						<xsl:attribute name="to">
							<xsl:value-of select="@to" />
						</xsl:attribute>
						<xsl:choose>
							<xsl:when test="count(.//skip:condition) > 0">
								<xsl:copy-of select=".//skip:condition" />
							</xsl:when>
							<xsl:otherwise>
								<xsl:attribute name="condition">otherwise</xsl:attribute>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:element>
				</xsl:for-each>
				<!-- If we were able to do the above, we hav effectively "processed" the sequenceGuide, so we skip the next element -->
				<xsl:apply-templates select="following-sibling::*[2]" mode="removeSequenceGuides" />
			</xsl:when>
			<xsl:otherwise>
				<xsl:copy-of select="." />
				<xsl:apply-templates select="following-sibling::*[1]" mode="removeSequenceGuides" />
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="skip:Loop" mode="removeSequenceGuides">
		<skip:loop question="{@question}" from="{@from}" to="{following-sibling::*[1]/@to}" innerchild="{@innerchild}"></skip:loop>
		<xsl:apply-templates select="*" mode="removeSequenceGuides" />
		<xsl:apply-templates select="following-sibling::*[2]" mode="removeSequenceGuides" /> <!-- Jump one because we delete and merge the next link above -->
	</xsl:template>
	<xsl:template match="skip:sequenceGuide" mode="removeSequenceGuides">
		<xsl:copy-of select="." />
		<xsl:apply-templates select="following-sibling::*[1]" mode="removeSequenceGuides" />
	</xsl:template>
	
	<xsl:template match="sqbl:loop" mode="toSequenceGuides">
		<xsl:element name="skip:loop">
			<xsl:attribute name="question"><xsl:value-of select="@question"/></xsl:attribute> 
			<xsl:attribute name="from">
				<xsl:value-of select="@name" />
			</xsl:attribute>
			<xsl:attribute name="to">
				<xsl:choose>
					<xsl:when test="count(following-sibling::*) > 0">
						<xsl:value-of select="following-sibling::*[1]/@name" />
					</xsl:when>
					<xsl:otherwise>
						<!-- get the first next element THAT IS INSIDE THIS LOOP -->
						<xsl:for-each select="ancestor-or-self::*[count(following-sibling::*)>0 and attribute::id][1]">
							<xsl:value-of select="following-sibling::*[1]/@name" />
						</xsl:for-each>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:attribute>
			<xsl:apply-templates select="*" mode="toSequenceGuides" />
		</xsl:element>
	</xsl:template>
	<xsl:template match="sqbl:ConditionalTree" mode="toSequenceGuides">
		<!-- There is always a then, so we always will link
			to the then "child" -->
		<xsl:element name="skip:sequenceGuide">
			<xsl:attribute name="from">
				<xsl:value-of select="@name" />
			</xsl:attribute>
			<xsl:variable name="otherwiseCond" select="sqbl:SequenceGuide/sqbl:Otherwise/@branch"/>
			<xsl:for-each select="sqbl:Branch">
				<!--<xsl:for-each select="sqbl:Branch[
				(@name != $otherwiseCond and $otherwiseCond)
					or
					(not($otherwiseCond))
				]">-->
				<xsl:variable name="branchID" select="@name"/>
				<xsl:element name="skip:link">
					<xsl:attribute name="to">
						<xsl:value-of select="sqbl:BranchLogic/*[1]/@name" />
					</xsl:attribute>
					<xsl:for-each select="../sqbl:SequenceGuide/sqbl:Condition[@resultBranch = $branchID]">
						<xsl:element name="skip:and">
							<xsl:for-each select="sqbl:ValueOf">
								<xsl:element name="skip:condition">
									<xsl:attribute name="question"><xsl:value-of select="@question"/></xsl:attribute>
									<xsl:attribute name="comparator"><xsl:value-of select="@is"/></xsl:attribute>
									<xsl:attribute name="val"><xsl:value-of select="."/></xsl:attribute>
									<xsl:value-of select="."/>
								</xsl:element>
							</xsl:for-each>
						</xsl:element>
					</xsl:for-each>
				</xsl:element>
			</xsl:for-each>
			<!-- The tricky bit - is there an else or not? -->
			<xsl:choose>
				<xsl:when test="count(sqbl:SequenceGuide/sqbl:Otherwise) > 0">
					<xsl:element name="skip:link">
						<xsl:attribute name="to">
							<xsl:value-of select="sqbl:Branch[@name = $otherwiseCond]/sqbl:BranchLogic/*[1]/@name" />
						</xsl:attribute>
						<xsl:attribute name="condition">otherwise</xsl:attribute>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<!-- If there is no else, we just point to the next item -->
					<xsl:apply-templates select="." mode="makeLink" />
				</xsl:otherwise>
			</xsl:choose>
		</xsl:element>
		<xsl:apply-templates select="*" mode="toSequenceGuides" />
	</xsl:template>
	<xsl:template match="sqbl:Branch" mode="toSequenceGuides">
		<xsl:apply-templates select="sqbl:BranchLogic/*" mode="toSequenceGuides" />
	</xsl:template>
	<xsl:template match="sqbl:Question | sqbl:QuestionGroup" mode="toSequenceGuides">
		<xsl:apply-templates select="." mode="makeLink" />
	</xsl:template>
	<xsl:template match="sqbl:ModuleExitPoint" mode="toSequenceGuides">
		<xsl:apply-templates select="." mode="makeLink" />
		<xsl:element name="skip:link">
			<xsl:attribute name="from">
				<xsl:value-of select="@name" />
			</xsl:attribute>
			<xsl:attribute name="to">__End__</xsl:attribute>
			<xsl:attribute name="type">StopModule</xsl:attribute>
		</xsl:element>
	</xsl:template>
	<xsl:template match="sqbl:Statement" mode="toSequenceGuides">
		<xsl:apply-templates select="." mode="makeLink" />
	</xsl:template>
	<xsl:template match="sqbl:condition" mode="toSequenceGuides">
		<skip:condition question="{@question}">
			<xsl:value-of select="." />
		</skip:condition>
	</xsl:template>
	<xsl:template match="sqbl:ForLoop" mode="toSequenceGuides">
		<skip:Loop question="{@question}" from="{@name}" innerchild="{sqbl:LoopedLogic/*[1]/@name}"> 
			<xsl:apply-templates select="sqbl:LoopedLogic/*" mode="toSequenceGuides" />
		</skip:Loop>
		<xsl:apply-templates select="." mode="makeLink" />
	</xsl:template>
	
	<xsl:template match="*" mode="toSequenceGuides" />
	
	<xsl:template match="*" mode="makeLink">
		<xsl:element name="skip:link">
			<xsl:attribute name="from">
				<xsl:value-of select="@name" />
			</xsl:attribute>
			<xsl:attribute name="to">
				<xsl:choose>
					<xsl:when test="count(following-sibling::*) > 0">
						<xsl:value-of select="following-sibling::*[1]/@name" />
					</xsl:when>
					<xsl:otherwise>
						<!-- get the first next element -->
						<xsl:for-each
							select="ancestor::*[local-name() = 'ForLoop' or
							count(following-sibling::*)>0 and local-name()='ConditionalTree'][1]">
							<xsl:choose>
								<xsl:when test="local-name(.) = 'ForLoop'">
									<!-- this is how we catch paths that might jump out of loops,
										and later we force them to a 'dummy' path -->
									<xsl:value-of select="./@name" />
									<xsl:text>__LOOP_END</xsl:text>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="following-sibling::*[1]/@name" />
								</xsl:otherwise>
							</xsl:choose>
						</xsl:for-each>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:attribute>
		</xsl:element>
	</xsl:template>
</xsl:stylesheet>
