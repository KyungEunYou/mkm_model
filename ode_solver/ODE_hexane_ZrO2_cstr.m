format long
close all
M = zeros(20,20) ;
M(20,20) = 1 ;
optode = odeset('NonNegative',1:20,'Abstol',1E-45,'RelTol',1E-45); % ,'Mass',M

x = 0;
P_H2 = 10 ;%y(1)
P_hexane = 1 ;%y(2)
P_1hexene = 0 ;%y(3)
P_cis2hexene = 0 ;%y(4)
P_trans2hexene = 0 ;%y(5)
P_1propene = 0 ;%y(6)
P_propane = 0 ;%y(7)
y0 = [P_H2,P_hexane,P_1hexene,P_cis2hexene,P_trans2hexene,P_1propene,P_propane,1,0,0,0,0,0,0,0,0,0,0,0,0] ;
y0=transpose(y0);
[t,y]=ode15s(@Func_hexane_ZrO2_cstr,[0,5e3],y0,optode); 
loglog(t, y(:,1),t, y(:,2),t, y(:,3),t, y(:,4),t, y(:,5),t, y(:,6),t, y(:,7)) ;
title('Solution of balance Equation');
xlabel('time t'); ylabel('solution y');
l = legend('P_H2','P_hexane','P_1hexene','P_cis2hexene','P_trans2hexene','P_1propene','P_propane') ;
set(l,'Edgecolor',[1 1 1]);
y=y(end,:);
%%CM_y_balance
y_site_balance = y.* [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] ;
sum(y_site_balance)

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
  
  r = [ r1 r2 r3 r4 r5 r6 r7 r8 r9 r10 r11 r12 r13 r14 r15 r16 r17 r18 r19 r20 r21] ;
  for_r = [ r1f r2f r3f r4f r5f r6f r7f r8f r9f r10f r11f r12f r13f r14f r15f r16f r17f r18f r19f r20f r21f] ;
  rev_r = [ r1r r2r r3r r4r r5r r6r r7r r8r r9r r10r r11r r12r r13r r14r r15r r16r r17r r18r r19r r20r r21r] ;
  r=r';
  for_r=for_r';
  rev_r=rev_r';
  y=y';
  A={'rate','f_rate','r_rate'};
  B={'coverage'};
  file = 'MKM_ZrO2_hex1bar_H2_10bar_CSTR_tau1E1_alpha1E-3_rc_r21_2.xlsx' ;
  xlswrite(file, A,'rate','A1')
  xlswrite(file, B,'coverage','A1')
  xlswrite(file, y,'coverage','A2')
  xlswrite(file, r,'rate','A2')
  xlswrite(file, for_r,'rate','B2')
  xlswrite(file, rev_r,'rate','C2')
  