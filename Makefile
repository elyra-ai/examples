#
# Copyright 2021-2021 Elyra Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

.PHONY: help test-dependencies lint-scripts lint-notebooks lint

SHELL:=/bin/bash

help:
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

test-dependencies:
	@pip install -q -r test_requirements.txt

lint-scripts: test-dependencies
	flake8 .

lint-notebooks: test-dependencies
	nbqa flake8 --ignore=H102 binder/getting-started/*.ipynb
	nbqa flake8 --ignore=H102,E402 pipelines/*/*.ipynb

lint: lint-scripts lint-notebooks ## Run linters
