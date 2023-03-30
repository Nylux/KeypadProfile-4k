$(V).SILENT:

NAME := 'KeypadProfile'
SRCS := keypadProfile.py GUI.py layouts/mainMenu.py

MAIN_SCRIPT := GUI.py
INI:= processes.ini
ICON := favicon.ico
REQUIREMENTS := requirements.txt
SPEC := $(NAME).spec

BUILD_DIR := build/
DIST_DIR := dist/


.PHONY: all spec gui clean fclean run

$(NAME):run

setup:
	echo 'euh flemme mdrrr kekw'

run:
	python $(MAIN_SCRIPT)

spec:
	if [ -f $(SPEC) ]; then \
		echo '$(SPEC) already exists.'; \
	else \
		echo 'Writing $(SPEC)...'; \
		pyi-makespec --log-level ERROR -i $(ICON) --windowed --onefile $(SRCS) --name $(NAME); \
	fi

gui: spec
	echo 'Building executable...'
	pyinstaller --log-level ERROR --clean $(SPEC)
	cp $(INI) $(DIST_DIR)$(INI)
	cp $(ICON) $(DIST_DIR)$(ICON)
	echo 'Building archive...'
	7za a -tzip ./$(DIST_DIR)$(NAME).zip -r -y -bsp0 -bso0 ./$(DIST_DIR)$(NAME).exe ./$(DIST_DIR)$(ICON) ./$(DIST_DIR)$(INI)
	rm $(DIST_DIR)$(NAME).exe $(DIST_DIR)$(ICON) $(DIST_DIR)$(INI)
	echo 'Release built and packed into '$(DIST_DIR)' folder.'

clean:
	rm -rf $(BUILD_DIR) __pycache__
	if test -f $(SPEC); then rm $(SPEC); fi

fclean: clean
	rm -rf $(DIST_DIR)
