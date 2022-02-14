# -*- coding: utf-8 -*-
from __future__ import print_function
from pprint import pprint

# import os
# ENV = os.environ

ENV = {}

ENV['CLICOLOR_FORCE'] = 1
ENV['DEBUG'] = 1
ENV['DIRENV_DIR'] = '-/Users/fish/Dropbox/CLU'
ENV['DIRENV_FILE'] = '/Users/fish/Dropbox/CLU/.envrc'
ENV['EDITOR'] = '/opt/homebrew/bin/emacs --no-window-system'
ENV['GOPATH'] = '/Users/fish/go:'
ENV['GPG_TTY'] = '/dev/ttys004'
ENV['HISTCONTROL'] = 'ignoreboth'
ENV['HISTIGNORE'] = '&:[bf]g:exit:*>|*:*rm*-rf*'
ENV['HISTSIZE'] = 1000000
ENV['HISTTIMEFORMAT'] = '%F %T '
ENV['HOME'] = '/Users/fish'
ENV['HOMEBREW_CURL'] = '/opt/homebrew/bin/curl'
ENV['HOMEBREW_EDITOR'] = '/opt/homebrew/bin/mate'
ENV['HOMEBREW_GIT'] = '/opt/homebrew/bin/git'
ENV['HOMEBREW_INSTALL_BADGE'] = '\xe2\x9a\x97\xef\xb8\x8f'
ENV['HOMEBREW_NO_ANALYTICS'] = 1
ENV['HOMEBREW_NO_ENV_HINTS'] = 1
ENV['JAVA_HOME'] = '/opt/homebrew/Cellar/openjdk/17.0.2/libexec/openjdk.jdk/Contents/Home'
ENV['LANG'] = 'en_US.UTF-8'
ENV['LESS'] = '-r'
ENV['LOGNAME'] = 'fish'
ENV['LS_COLORS'] = 'no=00;38;5;244:rs=0:di=00;38;5;33:ln=01;38;5;37:mh=00:pi=48;5;230;38;5;136;01:so=48;5;230;38;5;136;01:do=48;5;230;38;5;136;01:bd=48;5;230;38;5;244;01:cd=48;5;230;38;5;244;01:or=48;5;235;38;5;160:su=48;5;160;38;5;230:sg=48;5;136;38;5;230:ca=30;41:tw=48;5;64;38;5;230:ow=48;5;235;38;5;33:st=48;5;33;38;5;230:ex=01;38;5;64:*.tar=00;38;5;61:*.tgz=01;38;5;61:*.arj=01;38;5;61:*.taz=01;38;5;61:*.lzh=01;38;5;61:*.lzma=01;38;5;61:*.tlz=01;38;5;61:*.txz=01;38;5;61:*.zip=01;38;5;61:*.z=01;38;5;61:*.Z=01;38;5;61:*.dz=01;38;5;61:*.gz=01;38;5;61:*.lz=01;38;5;61:*.xz=01;38;5;61:*.bz2=01;38;5;61:*.bz=01;38;5;61:*.tbz=01;38;5;61:*.tbz2=01;38;5;61:*.tz=01;38;5;61:*.deb=01;38;5;61:*.rpm=01;38;5;61:*.jar=01;38;5;61:*.rar=01;38;5;61:*.ace=01;38;5;61:*.zoo=01;38;5;61:*.cpio=01;38;5;61:*.7z=01;38;5;61:*.rz=01;38;5;61:*.apk=01;38;5;61:*.gem=01;38;5;61:*.jpg=00;38;5;136:*.JPG=00;38;5;136:*.jpeg=00;38;5;136:*.gif=00;38;5;136:*.bmp=00;38;5;136:*.pbm=00;38;5;136:*.pgm=00;38;5;136:*.ppm=00;38;5;136:*.tga=00;38;5;136:*.xbm=00;38;5;136:*.xpm=00;38;5;136:*.tif=00;38;5;136:*.tiff=00;38;5;136:*.png=00;38;5;136:*.svg=00;38;5;136:*.svgz=00;38;5;136:*.mng=00;38;5;136:*.pcx=00;38;5;136:*.dl=00;38;5;136:*.xcf=00;38;5;136:*.xwd=00;38;5;136:*.yuv=00;38;5;136:*.cgm=00;38;5;136:*.emf=00;38;5;136:*.eps=00;38;5;136:*.CR2=00;38;5;136:*.ico=00;38;5;136:*.tex=01;38;5;245:*.rdf=01;38;5;245:*.owl=01;38;5;245:*.n3=01;38;5;245:*.ttl=01;38;5;245:*.nt=01;38;5;245:*.torrent=01;38;5;245:*.xml=01;38;5;245:*Makefile=01;38;5;245:*Rakefile=01;38;5;245:*build.xml=01;38;5;245:*rc=01;38;5;245:*1=01;38;5;245:*.nfo=01;38;5;245:*README=01;38;5;245:*README.txt=01;38;5;245:*readme.txt=01;38;5;245:*.md=01;38;5;245:*README.markdown=01;38;5;245:*.ini=01;38;5;245:*.yml=01;38;5;245:*.cfg=01;38;5;245:*.conf=01;38;5;245:*.c=01;38;5;245:*.cpp=01;38;5;245:*.cc=01;38;5;245:*.log=00;38;5;240:*.bak=00;38;5;240:*.aux=00;38;5;240:*.lof=00;38;5;240:*.lol=00;38;5;240:*.lot=00;38;5;240:*.out=00;38;5;240:*.toc=00;38;5;240:*.bbl=00;38;5;240:*.blg=00;38;5;240:*~=00;38;5;240:*#=00;38;5;240:*.part=00;38;5;240:*.incomplete=00;38;5;240:*.swp=00;38;5;240:*.tmp=00;38;5;240:*.temp=00;38;5;240:*.o=00;38;5;240:*.pyc=00;38;5;240:*.class=00;38;5;240:*.cache=00;38;5;240:*.aac=00;38;5;166:*.au=00;38;5;166:*.flac=00;38;5;166:*.mid=00;38;5;166:*.midi=00;38;5;166:*.mka=00;38;5;166:*.mp3=00;38;5;166:*.mpc=00;38;5;166:*.ogg=00;38;5;166:*.ra=00;38;5;166:*.wav=00;38;5;166:*.m4a=00;38;5;166:*.axa=00;38;5;166:*.oga=00;38;5;166:*.spx=00;38;5;166:*.xspf=00;38;5;166:*.mov=01;38;5;166:*.mpg=01;38;5;166:*.mpeg=01;38;5;166:*.m2v=01;38;5;166:*.mkv=01;38;5;166:*.ogm=01;38;5;166:*.mp4=01;38;5;166:*.m4v=01;38;5;166:*.mp4v=01;38;5;166:*.vob=01;38;5;166:*.qt=01;38;5;166:*.nuv=01;38;5;166:*.wmv=01;38;5;166:*.asf=01;38;5;166:*.rm=01;38;5;166:*.rmvb=01;38;5;166:*.flc=01;38;5;166:*.avi=01;38;5;166:*.fli=01;38;5;166:*.flv=01;38;5;166:*.gl=01;38;5;166:*.m2ts=01;38;5;166:*.divx=01;38;5;166:*.webm=01;38;5;166:*.axv=01;38;5;166:*.anx=01;38;5;166:*.ogv=01;38;5;166:*.ogx=01;38;5;166:'
ENV['LaunchInstanceID'] = 'DE7285B1-55D2-4A94-9187-DD2442F4FCBB'
ENV['NODE_PATH'] = '/opt/homebrew/share/npm/lib/node_modules:/Users/fish/.node_modules:\n'
ENV['OLDPWD'] = '/Users/fish/Dropbox/CLU'
ENV['ORIGINAL_PATH'] = '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/Apple/usr/bin'
ENV['PAGER'] = 'less'
ENV['PATH'] = '/Users/fish/Dropbox/CLU/develop/bin:/opt/homebrew/opt/python/libexec/bin:/opt/homebrew/opt/ruby/bin:/Users/fish/.script-bin:/Users/fish/go/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/X11/bin'
ENV['PGDATA'] = '/opt/homebrew/var/postgres/ost2'
ENV['PIP_RESPECT_VIRTUALENV'] = 'true'
ENV['PKG_CONFIG_PATH'] = '/opt/X11/lib/pkgconfig:/opt/homebrew/lib/pkgconfig:'
ENV['PROJECT_BASE'] = '/Users/fish/Dropbox/CLU/CLU'
ENV['PROJECT_CODE'] = '/Users/fish/Dropbox/CLU/CLU/clu'
ENV['PROJECT_NAME'] = 'CLU'
ENV['PROJECT_ROOT'] = '/Users/fish/Dropbox/CLU'
ENV['PROJECT_VENV'] = '/Users/fish/Dropbox/CLU/develop'
ENV['PROMPT_COMMAND'] = '_direnv_hook;set_bash_prompt'
ENV['PWD'] = '/Users/fish/Dropbox/CLU/CLU'
ENV['SAVEHIST'] = 999999
ENV['SECURITYSESSIONID'] = '186ac'
ENV['SHELL'] = '/opt/homebrew/bin/bash'
ENV['SHLVL'] = 0
ENV['TERM'] = 'xterm-256color'
ENV['TERM_PROGRAM'] = 'Apple_Terminal'
ENV['TERM_PROGRAM_VERSION'] = 443
ENV['USER'] = 'fish'
ENV['VIRTUALENVWRAPPER_PYTHON'] = '/opt/homebrew/opt/python/libexec/bin/python'
ENV['VIRTUAL_ENV'] = '/Users/fish/Dropbox/CLU/develop'
ENV['XML_CATALOG_FILES'] = '/opt/homebrew/etc/xml/catalog'
ENV['XPC_FLAGS'] = '0x0'
ENV['XPC_SERVICE_NAME'] = 0
ENV['_'] = '/opt/homebrew/bin/direnv'
ENV['__CFBundleIdentifier'] = 'com.apple.Terminal'

pprint(ENV)