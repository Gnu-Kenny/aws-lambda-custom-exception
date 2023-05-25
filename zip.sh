#bin/bash

zip -r aws-lambda-custom-exception.zip ./ -x './dev/*' -x '*.md' -x '*.gitignore' -x './*.git/*' -x '*.sh' -x '.DS_Store' -x './idea/*'