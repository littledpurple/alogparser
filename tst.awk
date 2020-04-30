{
split($4,t,/[[ :\/]/)
    mthNr = sprintf("%02d",(index("JanFebMarAprMayJunJulAugSepOctNovDec",t[3])+2)/3)
    curTime = t[4] mthNr t[2] t[5] t[6] t[7]
}
curTime >= minTime
