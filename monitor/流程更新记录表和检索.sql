
use rpa_vt;
-- 创建执行记录表
-- 按周统计每个设备的PASS，fail,image-count 数据, 有效数据 Image_count > 0

SELECT  week(create_time) as weekID, equipment_number, sum(image_count) as weekImage,sum(fail_count), sum(pass_count) FROM pmi_fail_record where  image_count >0 and (fail_count + pass_count = image_count) 
GROUP by weekID,equipment_number ORDER BY  weekID, weekImage DESC ;

-- 按周统计每个产品的PASS，fail,image-count 数据, 有效数据 Image_count > 0
SELECT  week(create_time) as weekID, device_name , sum(image_count) as weekImage,sum(fail_count), sum(pass_count) FROM pmi_fail_record where  image_count >0 and (fail_count + pass_count = image_count) 
GROUP by weekID,device_name ORDER BY  weekID, weekImage DESC ;


CREATE TABLE IF NOT EXISTS flow_target_record (
`device_num`	            VARCHAR(255),          /*-- 设备编号， POS-146                             */
`device_name`	            VARCHAR(255),          /*-- 产品名称， SHW                                 */
`lot`	                    VARCHAR(50),           /*-- Lot编号，  EQH837                              */
`wafer`	                VARCHAR(50),               /*-- wafer编号  EQH837-07-E2                        */
`wafer_start_time`	    DATETIME,                  /*-- wafer换片时间                                  */
`mark_align_ok_time`	    DATETIME,              /*-- 扫片完成时间                                   */
`stop_before_probe_time`	DATETIME,              /*-- 测前停止时间                                   */
`start_time`	            DATETIME,              /*-- 特征点比对开始时间                             */
`end_time`	            DATETIME,                  /*-- 特征点比对完成时间                             */
`cost`	                INT,                       /*-- 比对操作花费时间，单位：秒                     */
`H-F`	                    INT,                   /*-- 扫片完成到启动比对流程的时间间隔，单位：秒     */
`H-G`	                    INT,                   /*-- 测前停止发生到启动比对流程的时间间隔，单位：秒 */	
`I-H`	                    INT,                   /*-- 比对耗时，单位：秒	                           */
`E-F`	                    INT                    /*-- 换片到扫片完成的时间间隔，单位：秒             */
);


select * from target_local where end_time >0 and (device_name LIKE "%CDC%"  or device_name LIKE "%SHW%"  )group by lot  ORDER BY end_time DESC;
select * from target_local where end_time >0 and (device_name LIKE "%CDC%"  or device_name LIKE "%SHW%" )  ORDER BY end_time DESC;

select * from flow_target_record where end_time >0  group by lot  ORDER BY end_time DESC;
select * from flow_target_record where device_name LIKE "%CDC%"  or device_name LIKE "%SHW%"  group by lot  ORDER BY start_time DESC;

select * from flow_target_record where end_time IS NULL group by lot  ORDER BY start_time DESC;
select * from flow_target_record where start_time IS NOT NULL and mark_align_ok_time is not NULL  group by lot ORDER BY start_time DESC;

/*更新记录表*/
CREATE TABLE IF NOT EXISTS flow_update_record (
`fab`                       VARCHAR(255),          /*-- 区域，                             */ 
`StationID`	                VARCHAR(50),           /*-- 站点编号                               */
`AgentVersion`	            VARCHAR(50),           /*-- 客户端版本                             */
`AgentName`	                VARCHAR(255),          /*-- 客户端名称，                           */
`StationIP`	                VARCHAR(50),           /*-- 站点地址                                  */
`FlowName`	                VARCHAR(255),          /*-- 流程名称，                             */
`FlowVersion`	            VARCHAR(50),           /*-- 流程版本，                             */
`OtherStationID`	        VARCHAR(50),           /*-- 相关设备编号                                   */
`OtherStationIP`	        VARCHAR(50),           /*-- 相关设备地址                                   */
`UpdateTime`	            DATETIME,              /*-- 更新时间                             */
`UpdateStatus`	            VARCHAR(50),           /*-- 更新状态                        */
`Info`	                    VARCHAR(255),            /*-- 备注信息                     */
`account`	                VARCHAR(50)            /*-- 账号     */
);
-- DROP table flow_update_record;
DELETE FROM flow_update_record;
select * from flow_update_record fur ;

INSERT INTO flow_update_record (('fab', 'StationID', 'AgentVersion', 'AgentName', 'StationIP', 'FlowName', 'FlowVersion', 'OtherStationID', 'OtherStationIP', 'UpdateTime', 'UpdateStatus', 'Info', 'account', 'stationID')) VALUES (1.0, '', '1.1.0', '', '', '', '', '', '', '2024-07-04 01:06:29', '', '', '', 'POS-01');