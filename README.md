# 동적분석을 통한 안드로이드 어플리케이션의 적대적 테크닉 및 프로시저 탐지
### Adversarial Techniques and Procedure Detection for Android Applications through Dynamic Analysis


# Description
현재 안드로이드 malware 탐지에 관한 연구는 머신러닝을 통한 malware 탐지 성능 향상에 초점이 맞춰져있다.
그 결과 malware에 대한 탐지 성능은 매우 높아졌지만, 어떤 이유로 malware로 분류되었는지는 제대로 밝히지 못하는 한계점이 존재한다.

애플리케이션이 malware인지 아닌지 판단하는데 있어 가장 중요한 것은 애플리케이션의 행동(프로시저)이다.

MITRE ATT&CK에서는 포괄적인 최신 공격들을 전술, 테크닉, 프로시저로 분류하여 [Matrix](https://attack.mitre.org/versions/v12/matrices/mobile/android/)형태로 표현하고, 최신 공격들에 대한 탐지 및 공격 완화 기법 등의 정보를 제공한다.

[Quark](https://github.com/quark-engine/quark-engine)는 정적분석을 통해 테크닉 및 프로시저를 탐지하는 모듈이다.
이들은 [Androguard](https://androguard.readthedocs.io/en/latest/#)를 활용한 정적 분석을 통해 애플리케이션에서 호출한 API들을 분석하여 
규칙에 해당하는 API 호출 시퀀스가 존재하는지 판단한다.

Quark는 짧은 실행시간 내에 많은 애플리케이션들을 분석할 수 있지만 정적분석의 한계점에 의해 실제 호출에 사용된 인자 및 API 호출 시퀀스 분석의 정확성이 떨어진다.
이러한 한계점을 해결하기 위해 본 모델은 API 후킹과 동적분석을 통해 디테일한 API 호출 리스트를 추출하여 애플리케이션의 적대적 테크닉 및 프로시저를 판단한다.

# Detection Procedure
![image](https://user-images.githubusercontent.com/45464572/220097744-84af4bdc-9ab0-43bf-8c05-44c28d3b6784.png)

### 1. Load json rules
사전에 정의한 json 형태의 프로시저 규칙들을 로드한다.

### 2. Extract Permissions
입력으로 들어온 애플리케이션의 요구 권한을 추출한다.

### 3. Check Permission
각 프로시저마다 필요한 권한들이 존재하는지 확인한다. 만일 요구되는 권한이 모두 존재할 경우 적대적 행위가 가능할 것으로 판단, 해당 규칙들에 대해서는 동적 분석을 진행한다.

### 3.5 Dynamic Analysis
[frida](https://frida.re/)와 [droidbot](https://github.com/honeynet/droidbot)을 통해 애플리케이션을 동적분석하여 핵심 API들의 디테일한 호출을 추출한다.

### 4. Check API sequence
3.5단계에서 얻어낸 핵심 API들의 디테일한 호출들을 분석하여 API 호출 시퀀스가 존재하는지 판단한다.

판단 기준은 다음과 같다.
#### 1. 악성 행위에 요구되는 인자를 사용하였는가?
#### 2. 각 규칙에 해당하는 대로 호출이 이루어 졌는가? 

- 이전 depth의 API를 호출한 객체가 현 depth의 API를 호출하는 객체와 동일한가?
- 이전 dpeth의 API를 호출한 객체가 현 dpeth의 API의 인자로 사용되었는가?
- 이전 depth의 API를 통해 반환된 값/객체가 현 depth의 API를 호출하는 객체로 사용되었는가?

### 5. Report
4에서 확인한 내용을 토대로 어떤 프로시저들이 탐지되었는지를 출력한다.

# How to use
추가 예정

# Limitation
### 1. Number of Rules
아직 프로시저에 대한 분석이 많이 진행되지 않아 많은 규칙들을 생성하지 못하였다.

이 부분은 향후 추가적인 malware 분석을 통해 얻은 프로시저를 바탕으로 규칙들을 생성하고 추가하여 극복할 예정이다.

### 2. Dynamic Analysis
droidbot은 애플리케이션을 직접 실행하고 현재 상태(디스플레이)를 기반으로 랜덤한 입력 값을 주어 어떤 동작을 수행하는지 확인한다.

따라서 수행 시간이 길어지면 더욱 정확한 결과를 얻을 수 있지만, 많은 애플리케이션을 분석하는 것에는 적합하지 않은 방식이다.

또한 애플리케이션에 존재하는 코드라도 동적분석 동안 트리거되지 않는다면 분석할 수 없다는 한계점이 존재한다.

### 3. Malware Detection
현재 모델은 애플리케이션이 어떤 적대적 테크닉 및 프로시저를 수행하는지를 탐지하는데 초점이 맞춰져 있다.

하지만 가장 중요한 것은 행위 탐지보다 탐지된 행위를 통해 malware 여부를 판단하는 것이므로 해당 부분에 대한 연구가 추가적으로 필요하다.
  
