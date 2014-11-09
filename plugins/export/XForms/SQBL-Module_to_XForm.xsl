<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:exslt="http://exslt.org/common" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:fn="http://www.w3.org/2005/xpath-functions" xmlns:sqbl="sqbl:1" xmlns:qwac="qwac:reusable:1"
	xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:xf="http://www.w3.org/2002/xforms"
	xmlns:ev="http://www.w3.org/2001/xml-events" 
	xmlns:skip="http://legostormtoopr/skips" xmlns:cfg="rml:RamonaConfig_v1"
	exclude-result-prefixes="qwac exslt skip cfg" extension-element-prefixes="exslt">
	<!-- Import the XSLT for turning a responseML document into the skip patterns needed for conditional questions. -->
	<xsl:import href="../SQBL_to_Skips.xsl" />

	<!-- We are outputing XHTML so the output method will be XML, not HTML -->
	<xsl:output method="xml" />

	<!-- 
		Create the instrument for the XForms Model. This is represntation of the "true XML hierarchy" of the questionnaire (as opposed to the referential hiearchy of the DDI Document
		This is created as a global variable as it is needed in several different places for processing.
		The generated XML model of the questionnaire is needed for the data model of the final XForm, and exists as a ResponseML document.
	-->

	<xsl:variable name="skips">
		<xsl:call-template name="makeSkips">
			<xsl:with-param name="doc" select="//sqbl:ModuleLogic" />
		</xsl:call-template>
	</xsl:variable>

	<xsl:variable name="numbers">
		<xsl:for-each select="//*[local-name() != 'GroupedQuestions']/sqbl:Question | //sqbl:QuestionGroup">
			<xsl:element name="question">
				<xsl:attribute name="name">
					<xsl:value-of select="@name" />
				</xsl:attribute>
				<xsl:value-of select="position()" />
			</xsl:element>
		</xsl:for-each>
	</xsl:variable>

	<!-- 
		==============================
		MAIN ENTRY POINT FOR TRANSFORM
		==============================
		
		This template matches for the base module and creates the boiler plate for the final XHTML+XForms Document.
		It creates sections to hold a side menu linking within the page to all the major sections (div.majorsections), and main section for the survey itself (div.survey)
		There is the assumption that whatever calls this process will construct a DDI document with only one instrument.
		This assumption is based on the fact that only one survey instrument would be displayed to a respondent at a time.
		Prints the instrument name and description, and processes the single, valid ControlConstruct contained within the DDI Instrument.
	-->
	<xsl:template match="/">
		<!--xsl:processing-instruction name="xml-stylesheet">href="<xsl:value-of select="$rootdir"/>/xsltforms-beta2/xsltforms/xsltforms.xsl" type="text/xsl"</xsl:processing-instruction>
		<xsl:processing-instruction name="xsltforms-options">debug="no"</xsl:processing-instruction-->
		<html xmlns="http://www.w3.org/1999/xhtml" xmlns:xhtml="http://www.w3.org/1999/xhtml">
			<head>
				<title>
					<xsl:apply-templates select="sqbl:QuestionModule/sqbl:TextComponents/sqbl:TextComponent/sqbl:Title" />
				</title>
				<!-- Link to the CSS for rendering the form - ->
				<!-- Xforms Data model and bindings, including the ResponseML data instance. -->
				<xf:model>
					<xf:instance id="{//sqbl:QuestionModule/@name}">
						<xsl:apply-templates select="/sqbl:QuestionModule/sqbl:ModuleLogic" mode="makeDataModel"/>
					</xf:instance>
					<xf:instance id="decisionTables">
						<DecisionTables>
							<xsl:apply-templates select="/sqbl:QuestionModule/sqbl:ModuleLogic//sqbl:ConditionalTree" mode="makeDTs" />
						</DecisionTables>
					</xf:instance>
					<xf:instance id="wordsubs">
						<wordsubs>
							<xsl:apply-templates select="/sqbl:QuestionModule/sqbl:WordSubstitutions/sqbl:WordSub" mode="makeWordSubs" />
						</wordsubs>
					</xf:instance>
					<xsl:apply-templates select="//sqbl:ModuleLogic//sqbl:ConditionalTree | //sqbl:ModuleLogic//sqbl:Question | //sqbl:WordSub" mode="makeBindings"/>
					<xf:submission id="saveLocally" method="put" action="file://C:/temp/saved_survey.xml" />
					<!-- xf:submission id="saveRemotely" method="post"
						action="{$config/cfg:serverSubmitURI}"/ -->
					<!-- xf:submission id="debugDTs" method="put" ref="instance('decisionTables')//"
						action="file://C:/temp/saved_survey.xml" / -->
				</xf:model>
			</head>
			<body>
				<div id="survey">
					<h1>
						<xsl:apply-templates select="sqbl:QuestionModule/sqbl:TextComponents/sqbl:TextComponent/sqbl:Title" />
					</h1>
					<xsl:apply-templates select="//sqbl:ModuleLogic" />
					<!-- xf:submit submission="saveLocally">
						<xf:label>Save data locally</xf:label>
					</xf:submit -->
					<!-- xf:submit submission="debugDTs">
						<xf:label>Debug DTs</xf:label>
					</xf:submit -->
				</div>
			</body>
		</html>
	</xsl:template>

	<xsl:template match="sqbl:ModuleLogic">
		<xsl:apply-templates select="*" />
	</xsl:template>

	<xsl:template match="sqbl:Statement">
		<div class="statement">
		<xsl:attribute name="name">
			<xsl:value-of select="@name" />
		</xsl:attribute>
		<xsl:apply-templates select="./sqbl:TextComponent[@xml:lang='en']/sqbl:StatementText" />
		</div>
	</xsl:template>
	<!--
		Process IfThenElse Constructs and their child Then and Else elements.
		Both the Then and Else are wrapped in an XForms group. Then and Else get expressed as child XForms groups of this with bindings to allow or disallow response accordingly.
		Referenced ControlConstructs in the Then and Else blocks are then processed.
		At this point ElseIf constructs are ignored.
	-->
	<xsl:template match="sqbl:ConditionalTree">
		<xsl:apply-templates select="sqbl:Branch" />
	</xsl:template>
	<xsl:template match="sqbl:Branch">
		<xsl:element name="xf:group">
			<xsl:attribute name="bind">bind-<xsl:value-of select="@name" /></xsl:attribute>
			<xsl:apply-templates select="./sqbl:BranchLogic" />
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="sqbl:ForLoop">
		<strong>Start Loop <xsl:value-of select="@name"/></strong>
		<div/> <!-- This is bad, but loops are incloplete anyway. -->		
		<xsl:apply-templates select="sqbl:LoopedLogic/*" />
		<strong>End Loop <xsl:value-of select="@name"/></strong>		
	</xsl:template>

	<xsl:template match="sqbl:Instruction">
		<span class="Instruction">
			<xsl:value-of select="."/>
		</span>
	</xsl:template>
	<xsl:template match="sqbl:QuestionText | sqbl:StatementText">
		<xsl:apply-templates />
	</xsl:template>
	<xsl:template match="sqbl:sub">
		<strong>
			<xsl:variable name="ref" select="@ref"></xsl:variable>
			<xsl:choose>
				<xsl:when test="//sqbl:WordSub[@name=$ref]">
					<xsl:element name="xf:output">
						<xsl:attribute name="ref">instance('wordsubs')//*[@name='<xsl:value-of select="$ref" />']/*[@active=true()][1]</xsl:attribute>
					</xsl:element>
				</xsl:when>
				<xsl:when test="//sqbl:ForLoop[@name=$ref]">
					
				</xsl:when>
				<xsl:when test="//sqbl:Question[@name=$ref]">
					<xsl:element name="xf:output">
						<xsl:attribute name="ref">instance('<xsl:value-of select="//sqbl:QuestionModule/@name"/>')//*[@name='<xsl:value-of select="$ref" />']/*[1]</xsl:attribute>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					???
				</xsl:otherwise>
			</xsl:choose>
		</strong>
	</xsl:template>
	<xsl:template match="sqbl:em | sqbl:p">
		<xsl:variable name="tagname">
			<xsl:value-of select="local-name()"/>
		</xsl:variable>
		<xsl:element name="{$tagname}">
			<xsl:copy-of select="@*"/>
			<xsl:apply-templates select="* | text()"/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="sqbl:QuestionGroup">
		<xsl:variable name="qName" select="@name" />
		<span class="questionNumber">
			<xsl:value-of select="exslt:node-set($numbers)//question[@name=$qName]" />.
		</span>
		<div id="{@name}" class="roxyQuestionGroup">
			<span class="QuestionText">
				<xsl:apply-templates select="./sqbl:TextComponent[@xml:lang='en']/sqbl:QuestionText" />
			</span>
			<xsl:apply-templates select="./sqbl:TextComponent[@xml:lang='en']/sqbl:Instruction" />
			<ol>
				<xsl:for-each select="sqbl:GroupedQuestions/sqbl:Question">
					<li>
						<xsl:apply-templates select=".">
							<xsl:with-param name="inGroup" select="true()"/>
						</xsl:apply-templates>
					</li>
				</xsl:for-each>
			</ol>
		</div>
	</xsl:template>
	<xsl:template match="sqbl:Question">
		<xsl:param name="inGroup" select="false()"/>
		<xsl:if test="not($inGroup)">
			<xsl:variable name="qName" select="@name" />
			<span class="questionNumber">
				<xsl:value-of select="exslt:node-set($numbers)//question[@name=$qName]" />.
			</span>
		</xsl:if>
		<div id="{@name}" class="roxyQuestion">
			<span class="QuestionText">
				<xsl:apply-templates select="./sqbl:TextComponent[@xml:lang='en']/sqbl:QuestionText" />
			</span>
			<xsl:apply-templates select="./sqbl:TextComponent[@xml:lang='en']/sqbl:Instruction" />
			<div class="responses">
				<xsl:choose>
					<xsl:when test="count(./sqbl:SubQuestions/*) > 0 and count(sqbl:ResponseType/*) > 1">
						<table class="subQuestions">
							<tr>
								<th></th>
								<xsl:for-each select="sqbl:ResponseType/*">
									<th>
										<xsl:value-of select="./sqbl:Prefix/sqbl:TextComponent[@xml:lang='en']"/>
										<xsl:value-of select="./sqbl:Suffix/sqbl:TextComponent[@xml:lang='en']"/>
									</th>
								</xsl:for-each>
							</tr>
							<xsl:for-each select="sqbl:SubQuestions/sqbl:SubQuestion">
								<xsl:variable name="pos" select="position()"></xsl:variable>
								<tr>
									<td class="subQuestion">
										<xsl:apply-templates select="."/>
									</td>
									<xsl:for-each select="../../sqbl:ResponseType/*">
										<td>
											<xsl:apply-templates  select=".">
												<xsl:with-param name="subQuestionPosition" select="$pos"/>
											</xsl:apply-templates>
										</td>
									</xsl:for-each>
								</tr>
							</xsl:for-each>
						</table>
					</xsl:when>
					<xsl:when test="count(./sqbl:SubQuestions/*) > 0 and count(sqbl:ResponseType/*) = 1 and count(sqbl:ResponseType/sqbl:CodeList) = 1">
						<!-- that special case of subquestions with a codelist choice... -->
						<table class="subQuestions codelistTable">
							<tr>
								<th></th>
								<th>
								<xsl:for-each select="sqbl:ResponseType/sqbl:CodeList/sqbl:Codes/sqbl:CodePair">
									<span>
										<xsl:value-of select="./sqbl:TextComponent[@xml:lang='en']"/>
									</span>
								</xsl:for-each>
								</th>
							</tr>
							<xsl:for-each select="sqbl:SubQuestions/sqbl:SubQuestion">
								<xsl:variable name="pos" select="position()"></xsl:variable>
								<tr>
									<td class="subQuestion">
										<xsl:apply-templates select="."/>
									</td>
									<td>
										<xsl:for-each select="../../sqbl:ResponseType/sqbl:CodeList">
											<xsl:apply-templates select=".">
												<xsl:with-param name="subQuestionPosition" select="$pos"/>
												<xsl:with-param name="showNames" select="false()"/>
											</xsl:apply-templates>
										</xsl:for-each>
									</td>
								</tr>
							</xsl:for-each>
						</table>
					</xsl:when>
					<xsl:when test="count(./sqbl:SubQuestions/*) > 0">
						<ol class="subQuestions">
						<xsl:for-each select="sqbl:SubQuestions/sqbl:SubQuestion">
							<li>
							
								<span class="cell subQuestion">
									<xsl:apply-templates select="."/>
								</span>
								<xsl:for-each select="../../sqbl:ResponseType/*">
									<span class="cell">
										<xsl:apply-templates  select="."/>
									</span>
								</xsl:for-each>
							
							</li>
						</xsl:for-each>
						</ol>
					</xsl:when>
					<xsl:otherwise>
						<xsl:apply-templates  select="sqbl:ResponseType/*"/>
					</xsl:otherwise>
				</xsl:choose>
			</div>
		</div>
	</xsl:template>
	
	<xsl:template match="sqbl:SubQuestion">
		<xsl:value-of select="sqbl:TextComponent[@xml:lang='en']"/>
	</xsl:template>

	<xsl:template match="sqbl:CodeList">
		<xsl:param name="subQuestionPosition">XXX</xsl:param>
		<xsl:param name="showNames" select="true()"></xsl:param>
		
		<xsl:variable name="pos" select="position()"/>
		<xsl:variable name="selectionType">
			<xsl:choose>
				<xsl:when test="sqbl:MinimumSelections/@value > 1 or sqbl:MaximumSelections/@value > 1">
					<xsl:text>select</xsl:text>
				</xsl:when>
				<xsl:otherwise>
					<!-- If both of the selection flags are unset, it must be a single choice option set. -->
					<xsl:text>select1</xsl:text>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<!-- Inefficient, but doesn't require additional imports and works in Python/LXML -->
		<xsl:variable name="min">
			<xsl:choose>
				<xsl:when test="sqbl:MinimumSelections/@value >= 0">
					<xsl:choose>
						<xsl:when test="sqbl:MaximumSelections/@value > sqbl:MinimumSelections/@value">
							<xsl:value-of select="sqbl:MinimumSelections/@value"/>
						</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="sqbl:MaximumSelections/@value"/>
						</xsl:otherwise>
					</xsl:choose>					
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="1"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:variable name="max">
			<xsl:choose>
				<xsl:when test="sqbl:MaximumSelections/@value >= 0">
					<xsl:choose>
						<xsl:when test="sqbl:MaximumSelections/@value > sqbl:MinimumSelections/@value">
							<xsl:value-of select="sqbl:MaximumSelections/@value"/>
						</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="sqbl:MinimumSelections/@value"/>
						</xsl:otherwise>
					</xsl:choose>					
				</xsl:when>
				<xsl:otherwise>
					<xsl:choose>
						<xsl:when test="sqbl:MaximumSelections/@value >= 0 or sqbl:MinimumSelections/@value >= 0">
							<xsl:value-of select="count(../sqbl:Codes/sqbl:CodePair)"/>
						</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="1"/>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:element name="xf:{$selectionType}">
			<xsl:choose>
				<xsl:when test="$subQuestionPosition = 'XXX'">
					<xsl:attribute name="ref">instance('<xsl:value-of select="//sqbl:QuestionModule/@name"/>')//*[@name='<xsl:value-of select="../../@name" />']/*[<xsl:value-of select="$pos"/>]</xsl:attribute>
				</xsl:when>
				<xsl:otherwise>
					<xsl:attribute name="ref">instance('<xsl:value-of select="//sqbl:QuestionModule/@name"/>')//*[@name='<xsl:value-of select="../../@name" />']/*[<xsl:value-of select="$subQuestionPosition"/>]/*[<xsl:value-of select="$pos"/>]</xsl:attribute>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:attribute name="appearance">full</xsl:attribute>
			<xsl:if test="$showNames">
				<xf:label>
					<xsl:if test="$selectionType = 'select'">
						<xsl:choose>
							<xsl:when test="$min = $max">
								Select exactly <xsl:value-of select="$min"/>
							</xsl:when>
							<xsl:otherwise>
								<xsl:if test="$min > 0">
									Select at least <xsl:value-of select="$min"/>
								</xsl:if>
								<xsl:if test="$max > 0">
									Select at most <xsl:value-of select="$max"/>
								</xsl:if>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:if>
				</xf:label>
			</xsl:if>
			<xsl:for-each select="./sqbl:Codes/sqbl:CodePair">
				<xsl:element name="xf:item">
					<xsl:element name="xf:label">
						<xsl:if test="$showNames">
							<xsl:value-of select="sqbl:TextComponent[@xml:lang='en']"/>
						</xsl:if>
						<xsl:variable name="name" select="../../../../@name"/>
						<xsl:if test="count(exslt:node-set($skips)/skip:skips2/skip:link[@from=$name]) > 1">
							<xsl:variable name="value" select="@code"/>
							<xsl:choose>
								<xsl:when test="exslt:node-set($skips)/skip:skips2/skip:link[@from = $name]/skip:condition[@val = $value]">
									<xsl:variable name="to"><xsl:value-of select="exslt:node-set($skips)/skip:skips2/skip:link[@from = $name]/skip:condition[@val = $value]/../@to"/></xsl:variable>
									<span class="skipStatement">
										Go to <xsl:element name="a">
											<xsl:attribute name="href">#<xsl:value-of select="$to"/></xsl:attribute>
											Question <xsl:value-of select="exslt:node-set($numbers)//question[@name = $to]"/>
										</xsl:element>
										
										<!-- xsl:element name="xf:group">
											<xsl:attribute name="bind">bindThen-<xsl:value-of select="exslt:node-set($skips)/skip:link[@from = $name and @condition = $value]/@ifID"/></xsl:attribute>
											<xsl:element name="span">
												<xsl:attribute name="class">skipStatement</xsl:attribute>
												<xsl:attribute name="id"></xsl:attribute>
												Go to <xsl:element name="a">
													<xsl:attribute name="href">#<xsl:value-of select="$to"/></xsl:attribute>
													Question <xsl:value-of select="exslt:node-set($numbers)/question[@qcID = $to]"/>
												</xsl:element>
											</xsl:element>
										</xsl:element -->
									</span>
								</xsl:when>
								<xsl:when test="exslt:node-set($skips)/skip:skips2/skip:link[@from = $name and @condition = 'otherwise']">
									<xsl:variable name="to"><xsl:value-of select="exslt:node-set($skips)/skip:skips2/skip:link[@from = $name and @condition = 'otherwise']/@to"/></xsl:variable>
									<span class="skipStatement">
										Go to <xsl:element name="a">
											<xsl:attribute name="href">#<xsl:value-of select="$to"/></xsl:attribute>
											Question <xsl:value-of select="exslt:node-set($numbers)/question[@name = $to]"/>
										</xsl:element>
										<!-- xsl:element name="xf:group">
											<xsl:attribute name="bind">bindElse-<xsl:value-of select="exslt:node-set($skips)/skip:link[@from = $name and @condition = 'otherwise']/@ifID"/></xsl:attribute>
											<xsl:element name="span">
												<xsl:attribute name="class">skipStatement</xsl:attribute>
												Go to <xsl:element name="a">
													<xsl:attribute name="href">#<xsl:value-of select="$to"/></xsl:attribute>
													Question <xsl:value-of select="exslt:node-set($numbers)/question[@qcID = $to]"/>
												</xsl:element>
											</xsl:element>
										</xsl:element -->
									</span>
								</xsl:when>
							</xsl:choose>
						</xsl:if>
						
					</xsl:element>
					<xsl:element name="xf:value">
						<xsl:value-of select="@code"/>
					</xsl:element>
				</xsl:element>
			</xsl:for-each>
		</xsl:element>
	</xsl:template>

	
	<xsl:template match="sqbl:Number">
		<xsl:param name="subQuestionPosition">XXX</xsl:param>
		<xsl:variable name="pos" select="position()"/>
		<span class="responsePrefix">
			<xsl:value-of select="./sqbl:Prefix/sqbl:TextComponent[@xml:lang='en']"/>
		</span>
		<xsl:element name="xf:input">
			<xsl:attribute name="class">numericRepsonse</xsl:attribute>
			<xsl:attribute name="type">xs:number</xsl:attribute>
			<xsl:attribute name="appearance">full</xsl:attribute>
			<xsl:choose>
				<xsl:when test="$subQuestionPosition = 'XXX'">
					<xsl:attribute name="ref">instance('<xsl:value-of select="//sqbl:QuestionModule/@name"/>')//*[@name='<xsl:value-of select="../../@name" />']/*[<xsl:value-of select="$pos"/>]</xsl:attribute>
				</xsl:when>
				<xsl:otherwise>
					<xsl:attribute name="ref">instance('<xsl:value-of select="//sqbl:QuestionModule/@name"/>')//*[@name='<xsl:value-of select="../../@name" />']/*[<xsl:value-of select="$subQuestionPosition"/>]/*[<xsl:value-of select="$pos"/>]</xsl:attribute>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:if test="./sqbl:Hint/sqbl:TextComponent[@xml:lang='en']">
				<xf:help>
					<xsl:value-of select="./sqbl:Hint/sqbl:TextComponent[@xml:lang='en']"></xsl:value-of>
				</xf:help>
			</xsl:if>
			<!-- xf:alert>
				<xsl:value-of select="./sqbl:Minimum/sqbl:TextComponent[@xml:lang='en']"></xsl:value-of>
				<br />
				<xsl:value-of select="./sqbl:Maximum/sqbl:TextComponent[@xml:lang='en']"></xsl:value-of>
			</xf:alert -->
		</xsl:element>
		<!-- xsl:element name="xf:output">
			<xsl:attribute name="ref">instance('errors')//*[@name='<xsl:value-of select="../@name" />']</xsl:attribute>
		</xsl:element -->
		<span class="responseSuffix">
			<xsl:value-of select="./sqbl:Suffix/sqbl:TextComponent[@xml:lang='en']"/>
		</span>
	</xsl:template>
	<xsl:template match="sqbl:Text">
		<xsl:element name="xf:input">
			<xsl:attribute name="ref">instance('<xsl:value-of select="//sqbl:QuestionModule/@name"/>')//*[@name='<xsl:value-of select="../../@name" />']/*[<xsl:value-of select="position()"/>]</xsl:attribute>
			<!-- xsl:attribute name="ref">//sqbl:Question[@name='<xsl:value-of select="@name" />']</xsl:attribute -->
			
			<xsl:variable name="name" select="@name" />
			<xsl:if test="./sqbl:Hint/sqbl:TextComponent[@xml:lang='en']">
				<xf:help>
					<xsl:value-of select="./sqbl:Hint/sqbl:TextComponent[@xml:lang='en']"></xsl:value-of>
				</xf:help>
			</xsl:if>
			<xsl:if test="count(exslt:node-set($skips)/skip:skips2/*[@from=$name]) > 1">
				<ul>
					<xsl:for-each select="exslt:node-set($skips)/skip:skips2/*[@from=$name]">
						<li>
							<xsl:choose>
								<xsl:when test="@condition='otherwise'"> Otherwise </xsl:when>
								<xsl:otherwise> If <xsl:value-of select="skip:condition/@comparator" />
									'<xsl:value-of select="skip:condition" />' </xsl:otherwise>
							</xsl:choose> Go to <a href="#{@to}"><small><xsl:value-of select="@to" /></small></a>
						</li>
					</xsl:for-each>
				</ul>
			</xsl:if>
		</xsl:element>
	</xsl:template>

	<xsl:template match="*" mode="makeDTs" />
	<xsl:template match="sqbl:ConditionalTree" mode="makeDTs">
		<sqbl:SequenceGuide name="{@name}">
			<!-- The name is never used on this element, its just a sanity check for coders debuging the generated XForms -->
			<xsl:for-each select="sqbl:SequenceGuide/sqbl:Condition">
				<sqbl:Condition name="{@resultBranch}" />
			</xsl:for-each>
		</sqbl:SequenceGuide>
	</xsl:template>

	<xsl:template match="*" mode="makeBindings" />
	<xsl:template match="sqbl:ConditionalTree" mode="makeBindings">
		<xsl:apply-templates select="sqbl:SequenceGuide/sqbl:Condition" mode="makeBindings" />
		<xsl:apply-templates select="sqbl:Branch" mode="makeBindings" />
	</xsl:template>

	<xsl:template match="sqbl:SequenceGuide/sqbl:Condition" mode="makeBindings">
		<xsl:element name="xf:bind">
			<xsl:variable name="Bid">
				<xsl:value-of select="@resultBranch" />
			</xsl:variable>
			<xsl:attribute name="id">bind-SG-<xsl:value-of select="$Bid" />-<xsl:value-of select="position()" /></xsl:attribute>
			<xsl:attribute name="nodeset">instance('decisionTables')//*[@name='<xsl:value-of select="$Bid" />' and position()=<xsl:value-of select="position()" />]</xsl:attribute>
			<xsl:attribute name="calculate">
				<xsl:text>true()</xsl:text>
				<xsl:apply-templates select="sqbl:ValueOf" mode="makeBindings" />
			</xsl:attribute>
		</xsl:element>
	</xsl:template>

	<xsl:template match="sqbl:ValueOf" mode="makeBindings">
		<xsl:variable name="cond">
			<xsl:if test="@is = 'equal_to'">
				<xsl:text>=</xsl:text>
			</xsl:if>
			<xsl:if test="@is = 'not_equal_to'">
				<xsl:text>!=</xsl:text>
			</xsl:if>
			<xsl:if test="@is = 'less_than'">
				<xsl:text>&lt;</xsl:text>
			</xsl:if>
			<xsl:if test="@is = 'less_than_eq'">
				<xsl:text>&lt;=</xsl:text>
			</xsl:if>
			<xsl:if test="@is = 'greater_than'">
				<xsl:text>&gt;</xsl:text>
			</xsl:if>
			<xsl:if test="@is = 'greater_than_eq'">
				<xsl:text>&gt;=</xsl:text>
			</xsl:if>
			<!-- We can fix the next two later -->
			<xsl:if test="@is = 'inclusive_of'">
				<xsl:text>=</xsl:text>
			</xsl:if>
			<xsl:if test="@is = 'match_for'">
				<xsl:text>=</xsl:text>
			</xsl:if>
		</xsl:variable>
		<xsl:text /> and instance('<xsl:value-of select="//sqbl:QuestionModule/@name" />')//*[@name='<xsl:value-of select="@question" />'] <xsl:value-of select="$cond"/> '<xsl:value-of select="." />'<xsl:text />
	</xsl:template>
	<xsl:template match="sqbl:Branch" mode="makeBindings">
		<xsl:element name="xf:bind">
			<xsl:attribute name="id">bind-<xsl:value-of select="@name" /></xsl:attribute>
			<xsl:attribute name="nodeset">instance('<xsl:value-of select="//sqbl:QuestionModule/@name"/>')//*[@name='<xsl:value-of select="@name" />']</xsl:attribute>
			<xsl:attribute name="relevant">instance('decisionTables')//*[@name='<xsl:value-of select="@name" />'] = true()</xsl:attribute>
			<xsl:attribute name="readonly">not(instance('decisionTables')//*[@name='<xsl:value-of select="@name" />'] = true())</xsl:attribute>
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="sqbl:Question" mode="makeBindings">
		<xsl:apply-templates select="sqbl:ResponseType/*" mode="makeBindings"></xsl:apply-templates>
	</xsl:template>
	
	<xsl:template match="sqbl:ResponseType/sqbl:Number" mode="makeBindings">
		<xsl:element name="xf:bind">
			<xsl:attribute name="nodeset">instance('<xsl:value-of select="//sqbl:QuestionModule/@name"/>')//*[@name='<xsl:value-of select="../../@name" />']//sqbl:response[<xsl:value-of select="position()"/>]</xsl:attribute>
			<xsl:attribute name="type">xs:integer</xsl:attribute>
			<!-- xsl:attribute name="required"></xsl:attribute -->
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="*" mode="makeDataModel" />
		<!-- xsl:copy>
			<xsl:apply-templates select="@*|node()" mode="makeDataModel"/>
		</xsl:copy>
	</xsl:template -->
	
	<xsl:template match="sqbl:ModuleLogic" mode="makeDataModel">
		<sqbl:ModuleLogic>
			<xsl:apply-templates mode="makeDataModel"/>
		</sqbl:ModuleLogic>
	</xsl:template>
	<xsl:template match="sqbl:ConditionalTree" mode="makeDataModel">
		<sqbl:ConditionalTree name="{@name}">
			<xsl:apply-templates mode="makeDataModel"/>
		</sqbl:ConditionalTree>
	</xsl:template>
	<xsl:template match="sqbl:Branch" mode="makeDataModel">
		<sqbl:Branch name="{@name}">
			<xsl:apply-templates select="sqbl:BranchLogic/*" mode="makeDataModel"/>
		</sqbl:Branch>
	</xsl:template>
	<xsl:template match="sqbl:QuestionGroup" mode="makeDataModel">
		<sqbl:QuestionGroup name="{@name}">
			<xsl:apply-templates  select="sqbl:GroupedQuestions/*" mode="makeDataModel"/>
		</sqbl:QuestionGroup>
	</xsl:template>
	<xsl:template match="sqbl:Question" mode="makeDataModel">
		<sqbl:Question name="{@name}">
			<xsl:choose>
				<xsl:when test="count(./sqbl:SubQuestions/*) > 0">
					<xsl:for-each select="sqbl:SubQuestions/sqbl:SubQuestion">
						<xsl:element name="sqbl:SubQuestion">
							<xsl:apply-templates  select="../../sqbl:ResponseType/*" mode="makeDataModel"/>
						</xsl:element>
					</xsl:for-each>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates  select="sqbl:ResponseType/*" mode="makeDataModel"/>
				</xsl:otherwise>
			</xsl:choose>
		</sqbl:Question>
	</xsl:template>
	<xsl:template match="sqbl:Text | sqbl:Number | sqbl:CodeList"  mode="makeDataModel">
		<sqbl:response/>
	</xsl:template>
	<xsl:template match="sqbl:WordSub" mode="makeBindings">
		<xsl:apply-templates select="sqbl:Condition" mode="makeBindings"/>
	</xsl:template>
	<xsl:template match="sqbl:WordSub/sqbl:Condition" mode="makeBindings">
		<xsl:element name="xf:bind">
			<xsl:variable name="Bid">
				<xsl:value-of select="../@name" />
			</xsl:variable>
			<xsl:attribute name="id">bind-WS-<xsl:value-of select="$Bid" />-<xsl:value-of select="position()"/></xsl:attribute>
			<xsl:attribute name="nodeset">instance('wordsubs')//*[@name='<xsl:value-of select="$Bid" />']/*[@pos = <xsl:value-of select="position()" />]/@active</xsl:attribute>
			<xsl:attribute name="calculate">
				<xsl:text>true()</xsl:text>
				<xsl:apply-templates select="sqbl:ValueOf" mode="makeBindings" />
			</xsl:attribute>
		</xsl:element>
	</xsl:template>
	
	<!-- xsl:template match="sqbl:WordSub" mode="makeBindings">
		<xsl:element name="xf:bind">
			<xsl:attribute name="id">bind-<xsl:value-of select="@name" /></xsl:attribute>
			<xsl:attribute name="nodeset">instance('<xsl:value-of select="//sqbl:QuestionModule/@name"/>')//*[@name='<xsl:value-of select="@name" />']</xsl:attribute>
			<xsl:attribute name="relevant">instance('decisionTables')//*[@name='<xsl:value-of select="@name" />'] = true()</xsl:attribute>
			<xsl:attribute name="readonly">not(instance('decisionTables')//*[@name='<xsl:value-of select="@name" />'] = true())</xsl:attribute>
		</xsl:element>
	</xsl:template -->
	
	<xsl:template match="sqbl:WordSub" mode="makeWordSubs">
		<wordsub name="{@name}">
			<xsl:apply-templates select="sqbl:Condition" mode="makeWordSubs"/>
			<w active="true">
				<xsl:value-of select="./sqbl:TextComponent[@xml:lang='en']/sqbl:Default"/>
			</w>
		</wordsub>		
	</xsl:template>
	<xsl:template match="sqbl:Condition" mode="makeWordSubs">
		<w pos="{position()}" active="false">
			<xsl:apply-templates select="./sqbl:ResultString/sqbl:TextComponent[@xml:lang='en']" />
		</w>
	</xsl:template>
	<xsl:template match="sqbl:WordSub" mode="debug">
		<ol>
		<xsl:for-each select="sqbl:Condition">
		<li>
			<xsl:value-of select="../@name"/> =  '<xsl:element name="xf:output">
				<xsl:attribute name="ref">instance('wordsubs')//*[@name='<xsl:value-of select="../@name" />']/*[@pos=<xsl:value-of select="position()"/>]/@active</xsl:attribute>
			</xsl:element>'
		</li>
		</xsl:for-each>
		</ol>
	</xsl:template>
	
</xsl:stylesheet>
