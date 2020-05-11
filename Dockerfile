FROM python:latest
ARG app_folder=/usr/src/app
ARG regular_user=1000
ENV script_name=SendEmail.py
WORKDIR ${app_folder}
COPY ./${script_name} ./
USER root
RUN pip3 install requests && pip3 install pytz
USER ${regular_user}
CMD python3 ${script_name}

