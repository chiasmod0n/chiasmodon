FROM python:3.11-alpine

COPY . .
RUN python setup.py install

ENTRYPOINT [ "python3","/cli/chiasmodon_cli.py" ]