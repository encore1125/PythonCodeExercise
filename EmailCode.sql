/*Processed Raw Data*/
IF OBJECT_ID('tempdb..#RawData') is not null
BEGIN;
DROP Table #RawData;
END; 

SELECT 
      CONVERT(datetime, SUBSTRING (SUBSTRING([Date],0,CHARINDEX('-',[Date],0)) , 7, 100),105) AS EmailDate
      ,[From]
      --,[To]
	  , REPLACE(REPLACE (REPLACE (REPLACE([TO],'<','&lt;'), '>', '&gt;' ),'''','&#39;'),'"', '&quot;') AS [To]
	  , REPLACE(REPLACE (REPLACE (REPLACE([Cc],'<','&lt;'), '>', '&gt;' ),'''','&#39;'),'"', '&quot;') AS [Cc]
	  , REPLACE(REPLACE (REPLACE (REPLACE([Bcc],'<','&lt;'), '>', '&gt;' ),'''','&#39;'),'"', '&quot;') AS [Bcc]
      ,[Subject]
	  ,CASE WHEN [To] not like '%,%' and [Cc] is null and [BCc] is null THEN 'Direct'
	   WHEN  [To] like '%,%' OR [Cc] is not null OR [BCc] is not null THEN 'Broadcast'
	   END as Label --Label Direct or BoradCast email type
	into #RawData
  FROM [dbo].[EmailRawData]
  where [To] is not null --Some emails are missing To (Recipients) 



/*Split raw data to have To, Cc, Bcc recipients*/

IF OBJECT_ID('tempdb..#SplitData') is not null
BEGIN;
DROP Table #SplitData;
END; 

SELECT  EmailDate, 
        [Subject] ,
		[From], 
		[Recipients],
		Label into #SplitData FROM (

SELECT  EmailDate, 
        [Subject],
		[From],
        LTRIM(RTRIM(m.n.value('.[1]','varchar(8000)'))) AS [Recipients],
        Label
FROM
(
SELECT EmailDate, [Subject]  ,[From],
CAST('<XMLRoot><RowData>' + REPLACE([TO],',','</RowData><RowData>') + '</RowData></XMLRoot>' AS XML) AS x
,Label
FROM  #RawData 
)t
CROSS APPLY x.nodes('/XMLRoot/RowData')m(n) --Recipients from To

UNION ALL 

SELECT  EmailDate, 
        [Subject],
		[From],
        LTRIM(RTRIM(m.n.value('.[1]','varchar(8000)'))) AS [Recipients],
		Label
FROM
(
SELECT EmailDate, [Subject]  ,[From],
CAST('<XMLRoot><RowData>' + REPLACE([Cc],',','</RowData><RowData>') + '</RowData></XMLRoot>' AS XML) AS x
,Label
FROM   #RawData 
)t
CROSS APPLY x.nodes('/XMLRoot/RowData')m(n) --Recipients from Cc

UNION ALL

SELECT  EmailDate, 
        [Subject],
		[From],
        LTRIM(RTRIM(m.n.value('.[1]','varchar(8000)'))) AS [Recipients],
		Label
FROM
(
SELECT EmailDate, [Subject]  ,[From],
CAST('<XMLRoot><RowData>' + REPLACE([Bcc],',','</RowData><RowData>') + '</RowData></XMLRoot>' AS XML) AS x
,Label
FROM   #RawData
)t
CROSS APPLY x.nodes('/XMLRoot/RowData')m(n) ) as x --Recipients from Bcc

/*Formatted data */
IF OBJECT_ID('tempdb..#FormattedData') is not null
BEGIN;
DROP Table #FormattedData;
END; 

  SELECT DISTINCT EmailDate,
         LTRIM(RTRIM([Subject])) as [Subject],
		 LTRIM(RTRIM([From])) as [From] ,
		 LTRIM(RTRIM([Recipients])) as [Recipients],
		 Label  
		 into #FormattedData
		 FROM #SplitData
	

  /*Question1*/
 SELECT CAST(EmailDate as DATE) AS EmailDay, [Recipients], COUNT(*) AS Num FROM #FormattedData
 GROUP BY CAST(EmailDate as DATE), [Recipients]
-- HAVING COUNT(*) > 10 
 ORDER BY CAST(EmailDate as DATE) DESC




 /*Question2*/
 SELECT * FROM (
 SELECT [From] , Label , COUNT(*) AS RN FROM #FormattedData
 WHERE Label = 'Broadcast'
 GROUP BY [From] , Label ) AS X ORDER BY RN desc
 
 SELECT * FROM (
 SELECT  [Recipients], Label , COUNT(*) AS RN FROM #FormattedData
 WHERE Label = 'Direct'
 GROUP BY  [Recipients] , Label ) AS X ORDER BY RN desc



 /*Question3*/


SELECT  s1.[From] as OriginalSender,
        s1.[Recipients], 
		s1.EmailDate as OriginalEmailDate,
		r1.[From] as Replier, 
		r1.[Recipients], 
		r1.EmailDate as ResponseEmailDate , 
		s1.[subject] as OriginalSubject, 
		r1.[Subject] as ResponseSubject,
		DATEDIFF(minute,  s1.Emaildate , r1.EmailDate )  as ResponseTime 
FROM #FormattedData r1 
JOIN #FormattedData s1 on s1.[From] = r1.[Recipients] and r1.[From] = s1.[Recipients]
WHERE r1.[Subject] like '%' + s1.[Subject] + '%' --Response subject should contain orginal subject
AND r1.Subject <> '' --Removed some empty subject emails 
AND s1.Subject <> '' --Removed some empty subject emails 
AND s1.[From] <> S1.[Recipients]
AND R1.[From] <> R1.[Recipients] -- Removed the case Original sender also included in the sending list
AND s1.EmailDate < r1.EmailDate --Make sure response email later than orginal one
ORDER BY DATEDIFF(minute,  s1.Emaildate , r1.EmailDate ) --Five top 5 fast response
 
