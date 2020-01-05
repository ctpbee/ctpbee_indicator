from customize.api import (inited, O, H, L, C, volume, SMA, EMA, MA, KD, MACD, RSI, SMMA, ATR, STD, \
    BOLL, TRIX, ROC, MTM, TEMA, WR, CCI, SAR, HHV, LLV, REF, CROSS, SUM, ZIG, MIN)

CLOSE = C()
LOW = "LOW"
HIGH = "HIGH"

Var1 = (CLOSE-LLV(LOW, 36))/(HHV(HIGH, 36)-LLV(LOW, 36))*100
Var2 = SMA(Var1, 3, 1)
Var3 = SMA(Var2, 3, 1)
Var4 = SMA(Var3, 3, 1)
波: Var3
段: Var4
Var6 = CROSS(Var3, Var4) and Var3 < 20
Var7 = CROSS(Var4, Var3) and Var3 > 80
Var8 = CROSS(Var2, Var3) and Var3 > 80 and Var3 > Var4


# 通达信超人一号指标公式
# Var1:=(CLOSE-LLV(LOW,36))/(HHV(HIGH,36)-LLV(LOW,36))*100
# Var2:=SMA(Var1,3,1)
# Var3:=SMA(Var2,3,1)
# Var4:=SMA(Var3,3,1)
# 波: Var3
# 段: Var4
# Var6:=CROSS(Var3,Var4) AND Var3<20
# DRAWTEXT(FILTER(Var6,10)=1,40,'抄底'),LINETHICK3
# STICKLINE(FILTER(Var6,10)=1,0,30,10,0),COLORGREEN
# Var7:=CROSS(Var4,Var3) AND Var3>80;
# STICKLINE(FILTER(Var7,5)=1,80,100,10,0),COLORYELLOW
# DRAWTEXT(FILTER(Var7,5)=1,70,'逃顶'),LINETHICK3 ,COLORYELLOW
# Var8:=CROSS(Var2,Var3) AND Var3>80 AND Var3>Var4
# STICKLINE(Var8,85,100,10,0)