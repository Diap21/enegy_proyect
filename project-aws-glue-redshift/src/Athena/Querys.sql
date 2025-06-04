-- Tipo de energia más utilizado
SELECT ca.comunidad_autonoma, te.tipo_energia AS tipo_energia_mas_utilizado
FROM dim_com_aut ca
JOIN (
    SELECT t.id_comunidad, t.tipo_energia, 
           ROW_NUMBER() OVER (PARTITION BY t.id_comunidad ORDER BY COUNT(*) DESC) AS rn
    FROM processed t
    GROUP BY t.id_comunidad, t.tipo_energia
) te ON ca.id_comunidad = te.id_comunidad
WHERE te.rn = 1
GROUP BY ca.comunidad_autonoma,
         te.tipo_energia;                                        

--Patrón de consumo Energía renovable
SELECT ca.comunidad_autonoma,
       ROUND(
         SUM(CASE WHEN t.uso_energia_renovable = 'Si' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)
       , 2) AS porcentaje_renovable
FROM processed t
JOIN dim_com_aut ca ON t.id_comunidad = ca.id_comunidad
GROUP BY ca.comunidad_autonoma;               

--Consumo promedio de energia
SELECT p.provincia, round(AVG(t.consumo_kwh),2) AS consumo_promedio
FROM processed t
JOIN dim_provincia p ON t.id_provincia = p.id_provincia
GROUP BY p.provincia;             

--Factura promedio
SELECT te.tipo_energia, round(AVG(t.factura_mensual),2) AS factura_promedio
FROM processed t
JOIN dim_energia te ON t.id_tipo_energia = te.id_tipo_energia
GROUP BY te.tipo_energia;  