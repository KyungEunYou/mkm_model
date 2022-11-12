function F = Func_hexane_ZrO2_cstr(t,y)

P_H2 = 10 ;
P_hexane = 1 ;
alpha = 1E-3 ; 
tau = 1E1; 

Ptot = P_hexane + P_H2 ;

k1f = 308882374.60453707 ;
k1r = 40708184356.34481 ;
k2f = 47241341.380292386 ;
k2r = 1208714776.6944244 ;
k3f = 47804693.48340501 ;
k3r = 21331.746579144354 ;
k4f = 47804693.48340501 ;
k4r = 370.37281149843085 ;
k5f = 47804693.48340501 ;
k5r = 126195.32603269313 ;
k6f = 67606367.19006726 ;
k6r = 115231.96900112538 ;
k7f = 66039864.07344014 ;
k7r = 2913159237.4254136 ;
k8f = 67280567.71939887 ;
k8r = 2708718.318188459 ;
k9f = 79635.79059777372 ;
k9r = 2480715.277946526 ;
k10f = 452.198686686133 ;
k10r = 349883.71147431724 ;
k11f = 65.2133837948973 ;
k11r = 202954.352056259 ;
k12f = 0.0104653492231339 ;
k12r = 808.986288526249 ;
k13f = 14292.818634523674 ;
k13r = 216660.10650588205 ;
k14f = 2706.47227188065 ;
k14r = 1908.09570110115 ;
k15f = 68507.74321681082 ;
k15r = 89.76445807505995 ;
k16f = 70.10376057878543 ;
k16r = 18.11165237588549 ;
k17f = 89.9394792382428 ;
k17r = 0.20860691902856 ;
k18f = 396342.9795183338 ;
k18r = 57967.91427212642 ;
k19f = 69297896.1987754 ;
k19r = 90749.26352506006 ;
k20f = 1809.67480578015 ;
k20r = 7.00448218320178 ;
k21f = 4378.65108981979 ;
k21r = 1892.81984365143 ;

r1f=k1f*y(1)*power(y(8),1) ;
r1r=k1r*y(9) ;
r2f=k2f*y(2)*power(y(8),1) ;
r2r=k2r*y(10) ;
r3f=k3f*y(3)*power(y(8),1) ;
r3r=k3r*y(11) ;
r4f=k4f*y(4)*power(y(8),1) ;
r4r=k4r*y(12) ;
r5f=k5f*y(5)*power(y(8),1) ;
r5r=k5r*y(13) ;
r6f=k6f*y(6)*power(y(8),1) ;
r6r=k6r*y(14) ;
r7f=k7f*y(7)*power(y(8),1) ;
r7r=k7r*y(15) ;
r8f=k8f*power(y(9),1) ;
r8r=k8r*power(y(16),1) ;
r9f=k9f*power(y(10),1) ;
r9r=k9r*power(y(17),1) ;
r10f=k10f*power(y(10),1)*power(y(16),1) ;
r10r=k10r*power(y(17),1)*power(y(9),1) ;
r11f=k11f*power(y(10),1) ;
r11r=k11r*power(y(18),1) ;
r12f=k12f*power(y(10),1)*power(y(16),1) ;
r12r=k12r*power(y(18),1)*power(y(9),1) ;
r13f=k13f*power(y(17),1)*power(y(8),1) ;
r13r=k13r*power(y(11),1)*power(y(16),1) ;
r14f=k14f*power(y(18),1)*power(y(8),1) ;
r14r=k14r*power(y(11),1)*power(y(16),1) ;
r15f=k15f*power(y(18),1)*power(y(8),1) ;
r15r=k15r*power(y(12),1)*power(y(16),1) ;
r16f=k16f*power(y(18),1)*power(y(8),1) ;
r16r=k16r*power(y(13),1)*power(y(16),1) ;
r17f=k17f*power(y(18),1)*power(y(8),1) ;
r17r=k17r*power(y(19),1)*power(y(14),1) ;
r18f=k18f*power(y(19),1) ;
r18r=k18r*power(y(15),1) ;
r19f=k19f*power(y(20),1) ;
r19r=k19r*power(y(15),1) ;
r20f=k20f*power(y(14),1)*power(y(16),1) ;
r20r=k20r*power(y(19),1)*power(y(8),1) ;
r21f=k21f*power(y(14),1)*power(y(16),1) ;
r21r=k21r*power(y(20),1)*power(y(8),1) ;
r1=r1f-r1r ;
r2=r2f-r2r ;
r3=r3f-r3r ;
r4=r4f-r4r ;
r5=r5f-r5r ;
r6=r6f-r6r ;
r7=r7f-r7r ;
r8=r8f-r8r ;
r9=r9f-r9r ;
r10=r10f-r10r ;
r11=r11f-r11r ;
r12=r12f-r12r ;
r13=r13f-r13r ;
r14=r14f-r14r ;
r15=r15f-r15r ;
r16=r16f-r16r ;
r17=r17f-r17r ;
r18=r18f-r18r ;
r19=r19f-r19r ;
r20=r20f-r20r ;
r21=r21f-r21r ;

F = [ ;
(P_H2-y(1))/tau - y(1)*alpha*(-r1-r2-r3-r4-r5-r6-r7) + alpha*Ptot*(-r1) ;
(P_hexane-y(2))/tau - y(2)*alpha*(-r1-r2-r3-r4-r5-r6-r7) + alpha*Ptot*(-r2) ;
-y(3)/tau - y(3)*alpha*(-r1-r2-r3-r4-r5-r6-r7) + alpha*Ptot*(-r3) ;
-y(4)/tau - y(4)*alpha*(-r1-r2-r3-r4-r5-r6-r7) + alpha*Ptot*(-r4) ; 
-y(5)/tau - y(5)*alpha*(-r1-r2-r3-r4-r5-r6-r7) + alpha*Ptot*(-r5) ; 
-y(6)/tau - y(6)*alpha*(-r1-r2-r3-r4-r5-r6-r7) + alpha*Ptot*(-r6) ; 
-y(7)/tau - y(7)*alpha*(-r1-r2-r3-r4-r5-r6-r7) + alpha*Ptot*(-r7) ; 
-1*r1-1*r2-1*r3-1*r4-1*r5-1*r6-1*r7-1*r13-1*r14-1*r15-1*r16-1*r17+1*r20+1*r21 ;
1*r1-1*r8+1*r10+1*r12 ;
1*r2-1*r9-1*r10-1*r11-1*r12 ;
1*r3+1*r13+1*r14 ;
1*r4+1*r15 ;
1*r5+1*r16 ;
1*r6+1*r17-1*r20-1*r21 ;
1*r7+1*r18+1*r19 ;
1*r8-1*r10-1*r12+1*r13+1*r14+1*r15+1*r16-1*r20-1*r21 ;
1*r9+1*r10-1*r13 ;
1*r11+1*r12-1*r14-1*r15-1*r16-1*r17 ;
1*r17-1*r18+1*r20 ;
-1*r19+1*r21 ;
] ;
t
y
 
















