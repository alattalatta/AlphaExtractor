# AlphaExtractor - 알파추출기
Extracts strings of Rimworld mode file with custom nodes and Exports to language xml files.  
림월드 모드 파일의 노드를 추출하고, 사용자가 문자열들을 선택하여 language xml 파일로 출력할 수 있도록 해 줍니다.

# 오류 제보 및 개선사항
항상 두 팔 벌려 환영하고 있습니다.  
github의 Issues 메뉴를 이용해 사소한 오류부터 중대한 오류까지 모든 버그를 제보받고 있습니다.  
같은 방법으로 개선 사항을 받고 있습니다.  

# 버전 일람
## 0.8

* 0.8.4
  * `config.dat` 파일이 존재하지 않을 경우 (첫 실행 시) 프로그램이 실행되지 않는 현상이 해결되었습니다.

* 0.8.3
  * `병합하기`에서 추출되지 않은 노드가 삭제되는 현상이 해결되었습니다.  
  * 이제 `병합하기`모드에서 추출하지 않은 노드는 주석 처리되어 출력됩니다.

* 0.8.2
  * 이제 모든 필터(검색)에서 띄어쓰기와 대소문자 구분이 무시됩니다.  
  * 이제 분류한 태그 작업을 추후 재분류를 위해 저장/불러오기가 가능합니다.  
  * `TEST` 이제 list 태그는 분류 시 상위 태그로 분류되지만 출력은 해당하는 번호로 출력됩니다.  

* 0.8.1
  * 모드 선택창의 전반적인 개선이 이루어졌습니다.  
  * 이제 추출할 모드의 검색이 가능합니다.  
  * 이제 `LoadFolders.xml`의 모드 의존성 정보가 추출 선택창에 표시됩니다.  
  * 이제 서로 다른 버전의 다른 폴더들을 한꺼번에 추출할 수 있습니다. 노드의 중복이 발생할 경우, 위의 노드 텍스트는 아래의 노드 텍스트로 덮어씌워집니다.  
  * 이제 오류로 인해 추출되지 않던 `Strings`가 정상적으로 추출됩니다.  
  
* 0.8.0
  * 이제 `Defs` 외에도 `Keyed`와 `Strings`의 추출을 지원합니다. 

## 0.7
* 0.7.7
  * 이제 리스트 형태의 태그(숫자로 끝나는 태그)를 번역 가능한 형태로 추출할 수 있습니다. 
* 0.7.6
  * 파일 출력의 `건너뛰기` 옵션이 삭제되었습니다.  
  * 파일 출력의 텍스트 선택 모드에서 `원본`을 선택해도 다음 실행 시 `TODO`로 초기화되어 있는 현상을 수정하였습니다.  
  * `Patches`와 `Keyed` 등 여러 폴더를 지원하기 위해 코드의 구조가 개선되었습니다.  
* 0.7.5
  * 파일 출력의 `참조하기` 기능이 추가되었습니다. 해당 모드는 `추가하기` 모드와 유사하지만, 추출하지 않은 태그를 파일에 남기지 않습니다.  
  * 파일 출력의 여러 모드가 5개로 늘어남에 따라, 이제 각 선택지 위에 마우스를 올려 해당 모드의 설명을 나타내는 툴팁이 추가되었습니다.  
  * 이제 더 이상 태그 분류 작업을 확인하는 창이 뜨지 않습니다. 하지만 조심하세요! 태그 분류 작업 완료는 아직 되돌릴 수 없습니다!  
* 0.7.4
  * 파일 출력의 추가하기 모드를 사용했을 경우 파일이 출력되지 않거나 오류가 발생하는 문제를 해결했습니다.
* 0.7.3
  * 이제 파일 출력의 `추가하기` 모드에서 출력되는 태그들의 순서는 알파추출기가 새로 추출한 태그의 순서를 따릅니다.
* 0.7.2
  * 파일 출력 시 텍스트를 `{$TODO}` 대신 `TODO`로 출력합니다.  
* 0.7.1
  * 비정상적인 모드가 있을 경우 모드의 이름 대신 폴더의 이름을 로드합니다.
* 0.7
  * 이제 바닐라 번역에 등장하는 모든 태그들이 자동으로 추출 대상에 포함됩니다.  
  * 이제 태그 분류를 제외하고 입출력 폴더, 파일, 형식 등등의 모든 설정값이 저장되어 다음 실행시 유지됩니다.  

