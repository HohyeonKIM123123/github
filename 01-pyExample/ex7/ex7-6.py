

import ex7_6_mod

print(ex7_6_mod.add(10,20))
print(ex7_6_mod.sub(10,20))

print( ex7_6_mod. PI)

m = ex7_6_mod.Math()            # ✅ Math 클래스 객체 생성
print(m.solv(5))                # ✅ 원의 넓이 출력 (78.5398...)

from ex7_6_mod import add, sub

print(add (10,20))
