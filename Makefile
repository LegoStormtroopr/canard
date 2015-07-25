all : ui icons

ui :  windows widgets

windows: 
	pyuic4 ui/sqbl_main.ui -o SQBLWidgets/sqblUI/sqbl_main.py

widgets: 
	pyuic4 ui/SQBL_module_pane.ui -o SQBLWidgets/sqblUI/module_pane.py
	pyuic4 ui/branch.ui -o SQBLWidgets/sqblUI/branch.py
	pyuic4 ui/bulkQuestionEditor.ui -o SQBLWidgets/sqblUI/bulkQuestionEditor.py
	pyuic4 ui/conditionalTree.ui -o SQBLWidgets/sqblUI/conditionalTree.py
	pyuic4 ui/conditionalTreeText.ui -o SQBLWidgets/sqblUI/conditionalTreeText.py
	pyuic4 ui/derivedDataItems.ui -o SQBLWidgets/sqblUI/derivedDataItems.py
	pyuic4 ui/languagePicker.ui -o SQBLWidgets/sqblUI/languagePicker.py
	pyuic4 ui/logicNodeText.ui -o SQBLWidgets/sqblUI/logicNodeText.py
	pyuic4 ui/logicNodeText.ui -o SQBLWidgets/sqblUI/logicNodeText.py
	pyuic4 ui/loopFor.ui -o SQBLWidgets/sqblUI/loopFor.py
	pyuic4 ui/moduleLogic.ui -o SQBLWidgets/sqblUI/moduleLogic.py
	pyuic4 ui/newLanguageTab.ui -o SQBLWidgets/sqblUI/newLanguageTab.py
	pyuic4 ui/responseBoolean.ui -o SQBLWidgets/sqblUI/responseBoolean.py
	pyuic4 ui/responseCodeList.ui -o SQBLWidgets/sqblUI/responseCodeList.py
	pyuic4 ui/responseDate.ui -o SQBLWidgets/sqblUI/responseDate.py
	pyuic4 ui/responseGeneric.ui -o SQBLWidgets/sqblUI/responseGeneric.py
	pyuic4 ui/responseNumber.ui -o SQBLWidgets/sqblUI/responseNumber.py
	pyuic4 ui/responseText.ui -o SQBLWidgets/sqblUI/responseText.py
	pyuic4 ui/responseTime.ui -o SQBLWidgets/sqblUI/responseTime.py
	pyuic4 ui/responseTab.ui -o SQBLWidgets/sqblUI/responseTab.py
	pyuic4 ui/questionGroup.ui -o SQBLWidgets/sqblUI/questionGroup.py
	pyuic4 ui/questionModule.ui -o SQBLWidgets/sqblUI/questionModule.py
	pyuic4 ui/questionModuleText.ui -o SQBLWidgets/sqblUI/questionModuleText.py
	pyuic4 ui/questionText.ui -o SQBLWidgets/sqblUI/questionText.py
	pyuic4 ui/question.ui -o SQBLWidgets/sqblUI/question.py
	pyuic4 ui/population.ui -o SQBLWidgets/sqblUI/population.py
	pyuic4 ui/preferencesDialog.ui -o SQBLWidgets/sqblUI/preferencesDialog.py
	pyuic4 ui/statementText.ui -o SQBLWidgets/sqblUI/statementText.py
	pyuic4 ui/stopModule.ui -o SQBLWidgets/sqblUI/stopModule.py
	pyuic4 ui/statement.ui -o SQBLWidgets/sqblUI/statement.py
	pyuic4 ui/subQuestion.ui -o SQBLWidgets/sqblUI/subQuestion.py
	pyuic4 ui/unsupportedWidget.ui -o SQBLWidgets/sqblUI/unsupportedWidget.py
	pyuic4 ui/wordSub.ui -o SQBLWidgets/sqblUI/wordSub.py
	pyuic4 ui/wordSubText.ui -o SQBLWidgets/sqblUI/wordSubText.py
	pyuic4 ui/wordSubstitutions.ui -o SQBLWidgets/sqblUI/wordSubstitutions.py

#x.py: X.ui
#	pyuic ui/X.ui -o SQBLWidgets/sqblUI/x.py


# ICONS
#icons:
	pyrcc4 icons/canard.qrc -o SQBLWidgets/sqblUI/canard_rc.py

prepExe:
	cp -r icons dist/Canard/
	rm    dist/Canard/icons/Canard_icon.ico
	cp -r images dist/Canard/
	mkdir dist/Canard/roxy
	cp -r ../roxy-sqbl-instrument-creator/* dist/Canard/roxy/
	mkdir dist/Canard/sqbl
	cp -r ../sqbl-schema/Schemas/* dist/Canard/sqbl/
	mkdir dist/Canard/examples
	cp -r ../sqbl-schema/Tests/* dist/Canard/examples
	mkdir dist/Canard/plugins
	cp -r ./plugins/* dist/Canard/plugins

