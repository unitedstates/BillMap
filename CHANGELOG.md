# Changelog

## [v0.4.0](https://github.com/aih/FlatGov/tree/v0.4.0) (2021-05-25)

[Full Changelog](https://github.com/aih/FlatGov/compare/v0.3.1...v0.4.0)

**Fixed bugs:**

- 'No data available' statements not showing  [\#353](https://github.com/aih/FlatGov/issues/353)

**Closed issues:**

- Home and Bill Page - Change background color [\#394](https://github.com/aih/FlatGov/issues/394)
- Overview section and Committees and Sponsors section buttons should be positioned at the bottom of the sections [\#393](https://github.com/aih/FlatGov/issues/393)
- Cosponsors table 'This Congress' tab shows the full list of cosponsors [\#381](https://github.com/aih/FlatGov/issues/381)
- Normalize section total score for display [\#379](https://github.com/aih/FlatGov/issues/379)
- Metadata conversion not completed for some bills  [\#378](https://github.com/aih/FlatGov/issues/378)
- Cosponsors table shows a single sponsor of bills in both House and Senate [\#375](https://github.com/aih/FlatGov/issues/375)
- Add bill number \(e.g. 116hr200\) as a column in the CSV table for the CRS [\#364](https://github.com/aih/FlatGov/issues/364)
- Run CRS update + CSV as a nightly Celery task [\#363](https://github.com/aih/FlatGov/issues/363)
- For title matching, remove leading text of the form '117 HR 447 IH: ' [\#359](https://github.com/aih/FlatGov/issues/359)
- Add 'incorporated by' and 'incorporates' to relatedness criteria [\#355](https://github.com/aih/FlatGov/issues/355)
- Rename Context tabs [\#350](https://github.com/aih/FlatGov/issues/350)
- Develop About Us Page [\#348](https://github.com/aih/FlatGov/issues/348)
- Access to `crs/csv-report` times out \(we have ~6000 records\) [\#346](https://github.com/aih/FlatGov/issues/346)
- Review main and ensure enhancements have been added [\#344](https://github.com/aih/FlatGov/issues/344)
- Update docs and link to navigation bar [\#336](https://github.com/aih/FlatGov/issues/336)
- Issue with the logic of "Sponsors of Related Measures"  [\#326](https://github.com/aih/FlatGov/issues/326)
- Add column to indicate whether a cosponsor is no longer in Congress [\#322](https://github.com/aih/FlatGov/issues/322)
- Get cosponsors of related bills \(update\) [\#319](https://github.com/aih/FlatGov/issues/319)
- Create Celery task to update cosponsors and committees [\#298](https://github.com/aih/FlatGov/issues/298)
- Put examples of search formats below the search bar & changes to reflect wireframe [\#272](https://github.com/aih/FlatGov/issues/272)
- Scoring document similarity [\#267](https://github.com/aih/FlatGov/issues/267)
- Monthly View on Calendar should start on Monday [\#257](https://github.com/aih/FlatGov/issues/257)
- Add Text that explains that there is not a document available for Understand the Context Section [\#249](https://github.com/aih/FlatGov/issues/249)
- When the user is on a bill page, the Bill tab in the nav should be highlighted [\#245](https://github.com/aih/FlatGov/issues/245)
- Document the SAP scrapers for Trump and Biden [\#230](https://github.com/aih/FlatGov/issues/230)
- Understand the Context UI Fix [\#181](https://github.com/aih/FlatGov/issues/181)
- Future improvements for 'similar bills' [\#178](https://github.com/aih/FlatGov/issues/178)
- Add "Currently in Congress" column  to the "Sponsors of Related Measures" section [\#108](https://github.com/aih/FlatGov/issues/108)
- UI update for "Overview" section on the bill page [\#102](https://github.com/aih/FlatGov/issues/102)
- Bill title should be left aligned with all the boxes [\#100](https://github.com/aih/FlatGov/issues/100)
- Add "Compare" text button under the "Compare Bill Text" column.  [\#89](https://github.com/aih/FlatGov/issues/89)
- Change search UI on Home Page [\#83](https://github.com/aih/FlatGov/issues/83)
- The list of related bills in the top left panel does not always match the table of related bills [\#64](https://github.com/aih/FlatGov/issues/64)
- On the Bills page, change the order of tabs in the "Understand the Context" section  [\#63](https://github.com/aih/FlatGov/issues/63)
- Collect cboCostEstimates from data.json for each bill [\#53](https://github.com/aih/FlatGov/issues/53)
- Document the `bills` table and how it relates to govtrack tables [\#50](https://github.com/aih/FlatGov/issues/50)
- Sources for 'in Focus' information  [\#1](https://github.com/aih/FlatGov/issues/1)

**Merged pull requests:**

- Feature/buttons 393 [\#396](https://github.com/aih/FlatGov/pull/396) ([ayeshamk](https://github.com/ayeshamk))
- Feature/background 394 [\#395](https://github.com/aih/FlatGov/pull/395) ([ayeshamk](https://github.com/ayeshamk))
- Filter cosponsor by Congress \#381 [\#384](https://github.com/aih/FlatGov/pull/384) ([aih](https://github.com/aih))
- Fix for \#379. Normalize score [\#380](https://github.com/aih/FlatGov/pull/380) ([aih](https://github.com/aih))
- Fixes \#375 [\#376](https://github.com/aih/FlatGov/pull/376) ([aih](https://github.com/aih))
- Feature/simlar reasons update [\#374](https://github.com/aih/FlatGov/pull/374) ([aih](https://github.com/aih))
- Handle new 'reason' form [\#372](https://github.com/aih/FlatGov/pull/372) ([aih](https://github.com/aih))
- Update CSV writer for CRS [\#371](https://github.com/aih/FlatGov/pull/371) ([aih](https://github.com/aih))
- Fix 'Rank' column for cosponsors [\#370](https://github.com/aih/FlatGov/pull/370) ([aih](https://github.com/aih))
- home page UI changes [\#369](https://github.com/aih/FlatGov/pull/369) ([ayeshamk](https://github.com/ayeshamk))
- Feature/container UI changes ayesha [\#367](https://github.com/aih/FlatGov/pull/367) ([ayeshamk](https://github.com/ayeshamk))
- Feature/similarbills matrix [\#365](https://github.com/aih/FlatGov/pull/365) ([aih](https://github.com/aih))
- Weini [\#362](https://github.com/aih/FlatGov/pull/362) ([aih](https://github.com/aih))
- autocomplete and csv export updated [\#356](https://github.com/aih/FlatGov/pull/356) ([aih](https://github.com/aih))
- Feature/committees alignment fixed ayesha [\#354](https://github.com/aih/FlatGov/pull/354) ([ayeshamk](https://github.com/ayeshamk))
- Revert "Feature/no data msg2" [\#352](https://github.com/aih/FlatGov/pull/352) ([aih](https://github.com/aih))
- Feature/enhancements ayesha 2 [\#351](https://github.com/aih/FlatGov/pull/351) ([ayeshamk](https://github.com/ayeshamk))
- Fix calendar key [\#349](https://github.com/aih/FlatGov/pull/349) ([aih](https://github.com/aih))
- Feature/no data msg2 [\#347](https://github.com/aih/FlatGov/pull/347) ([aih](https://github.com/aih))
- Standardize styling when table does not have data [\#345](https://github.com/aih/FlatGov/pull/345) ([aih](https://github.com/aih))
- Fix calendar-key styling [\#343](https://github.com/aih/FlatGov/pull/343) ([aih](https://github.com/aih))
- Feature/enhancements cherrypick 2 [\#342](https://github.com/aih/FlatGov/pull/342) ([aih](https://github.com/aih))
- nav bar, home page and celery task is added [\#341](https://github.com/aih/FlatGov/pull/341) ([aih](https://github.com/aih))
- calendar UI changes [\#339](https://github.com/aih/FlatGov/pull/339) ([ayeshamk](https://github.com/ayeshamk))

## [v0.3.1](https://github.com/aih/FlatGov/tree/v0.3.1) (2021-05-01)

[Full Changelog](https://github.com/aih/FlatGov/compare/v0.3.0...v0.3.1)

**Implemented enhancements:**

- Create Celery task to update CBO data [\#213](https://github.com/aih/FlatGov/issues/213)

**Closed issues:**

- Daniel's Home Page Feedback [\#207](https://github.com/aih/FlatGov/issues/207)
- CRS reports: add a Celery task [\#173](https://github.com/aih/FlatGov/issues/173)
- UI Updates for Sponsors of Related Measures [\#147](https://github.com/aih/FlatGov/issues/147)

**Merged pull requests:**

- Docs/update and link [\#338](https://github.com/aih/FlatGov/pull/338) ([aih](https://github.com/aih))
- Docs/update and link [\#337](https://github.com/aih/FlatGov/pull/337) ([aih](https://github.com/aih))
- home UI updated [\#335](https://github.com/aih/FlatGov/pull/335) ([aih](https://github.com/aih))

## [v0.3.0](https://github.com/aih/FlatGov/tree/v0.3.0) (2021-04-27)

[Full Changelog](https://github.com/aih/FlatGov/compare/v0.2.1...v0.3.0)

**Implemented enhancements:**

- Move all scrapy scripts out of the top level of the `scrapers` directory [\#210](https://github.com/aih/FlatGov/issues/210)

**Fixed bugs:**

- Problem getting number for congress with some bills [\#329](https://github.com/aih/FlatGov/issues/329)
- CBO report: handle error with 'pubDate' [\#184](https://github.com/aih/FlatGov/issues/184)
- Skip adding text when there is no summary \(adding cosponsors\) [\#55](https://github.com/aih/FlatGov/issues/55)
- Apparent problem indexing 116hr5150 [\#43](https://github.com/aih/FlatGov/issues/43)
- Handle cosponsor names like 'Sanford D. Bishop, Jr.' which currently becomes 'Jr. Sanford D. Bishop' [\#24](https://github.com/aih/FlatGov/issues/24)

**Closed issues:**

- Search using just the bill number will populate results but the links route the user to a "page not found" page [\#327](https://github.com/aih/FlatGov/issues/327)
- Develop a download csv/xls file feature for the "Sponsors of related measures" table data [\#324](https://github.com/aih/FlatGov/issues/324)
- Remove Committee Id from both Cosponsors tables [\#323](https://github.com/aih/FlatGov/issues/323)
- Change 'On Assigned Committee' to 'Current Assigned Committee' [\#321](https://github.com/aih/FlatGov/issues/321)
- Add 'leadership' information to Cosponsor download [\#316](https://github.com/aih/FlatGov/issues/316)
- Remove 'Read Bill:' text [\#313](https://github.com/aih/FlatGov/issues/313)
- Short title missing in bill data [\#309](https://github.com/aih/FlatGov/issues/309)
- Set the order of cosponsors for the Committees and Cosponsors box [\#306](https://github.com/aih/FlatGov/issues/306)
- Propagate Cosponsor table to the `cosponsor_dict` in the detail.html view [\#305](https://github.com/aih/FlatGov/issues/305)
- Handle 'H.Con.Res.' in title correctly [\#304](https://github.com/aih/FlatGov/issues/304)
- Capture committee information when processing data.json for bills [\#300](https://github.com/aih/FlatGov/issues/300)
- Related Bills in Overview section - include only related bills from the current congress and change display [\#290](https://github.com/aih/FlatGov/issues/290)
- Apply ordinal in bill display filter  [\#289](https://github.com/aih/FlatGov/issues/289)
- Press statement Put Pagination in a fixed position [\#283](https://github.com/aih/FlatGov/issues/283)
- Press statements: Add Pagination navigation menu [\#281](https://github.com/aih/FlatGov/issues/281)
- Press Statements: Change architecture and show results instantly using direct API calls [\#280](https://github.com/aih/FlatGov/issues/280)
- Press Statements  [\#275](https://github.com/aih/FlatGov/issues/275)
- Read Bill button  [\#274](https://github.com/aih/FlatGov/issues/274)
- Include short title \(or truncated short title\) in typeahead search list [\#273](https://github.com/aih/FlatGov/issues/273)
- Search bar input format [\#271](https://github.com/aih/FlatGov/issues/271)
- The congress filter should be on the same line as the search bar and include arrow [\#270](https://github.com/aih/FlatGov/issues/270)
- Create scraper to update legislator information [\#268](https://github.com/aih/FlatGov/issues/268)
- Create a Celery task to update the \(Biden\) SAP scraper daily  [\#264](https://github.com/aih/FlatGov/issues/264)
- Committee and member information available from Propublica API [\#263](https://github.com/aih/FlatGov/issues/263)
- Add Committee and Party information to Sponsors [\#259](https://github.com/aih/FlatGov/issues/259)
- Provide consistent bill number display, e.g. H. R. 1500 \(116\) [\#254](https://github.com/aih/FlatGov/issues/254)
- Organize Celery tasks [\#248](https://github.com/aih/FlatGov/issues/248)
- Make Sponsor table more compatible with Govtrack [\#228](https://github.com/aih/FlatGov/issues/228)
- Remove the 'Sponsor' model from bill.models [\#227](https://github.com/aih/FlatGov/issues/227)
- Refactor CBO scraper to allow dynamic updates [\#212](https://github.com/aih/FlatGov/issues/212)
- Create Celery task for Committee Documents [\#205](https://github.com/aih/FlatGov/issues/205)
- Scrape the current Biden Statements of administration policy [\#203](https://github.com/aih/FlatGov/issues/203)
- Statements and CBO: Consider using many-to-many relation to bills [\#185](https://github.com/aih/FlatGov/issues/185)
- UI Sprint 1 \_ Bill Page "Folder" Containers [\#166](https://github.com/aih/FlatGov/issues/166)
- UI Sprint 1 \_ Bills Related to  [\#164](https://github.com/aih/FlatGov/issues/164)
- UI Sprint 1 \_ Committees and Sponsors Section [\#163](https://github.com/aih/FlatGov/issues/163)
- UI Sprint 1 \_ Overview Section  [\#161](https://github.com/aih/FlatGov/issues/161)
- Change Overview Section UI [\#155](https://github.com/aih/FlatGov/issues/155)
- Bill selection: Allow user to hit return to select the currently typed value [\#123](https://github.com/aih/FlatGov/issues/123)
- Bill summary should be a small description instead of a "read bill" button [\#101](https://github.com/aih/FlatGov/issues/101)
- Add "Export" button on right side for "Sponsors of Related Measures" and " Bills Related to" sections to download a .csv file [\#90](https://github.com/aih/FlatGov/issues/90)
- Link to Committee transcript data for bill \(no need to scrape\) [\#54](https://github.com/aih/FlatGov/issues/54)
- Develop API calls for Press statements [\#35](https://github.com/aih/FlatGov/issues/35)

**Merged pull requests:**

- Remove 'amdt' bills from search. Fixes \#327 [\#332](https://github.com/aih/FlatGov/pull/332) ([aih](https://github.com/aih))
- Feature/related cosponsors [\#331](https://github.com/aih/FlatGov/pull/331) ([aih](https://github.com/aih))
- Fix for 'None' in bill number or congress [\#330](https://github.com/aih/FlatGov/pull/330) ([aih](https://github.com/aih))
- Feature/committees cosponsors ayesha [\#328](https://github.com/aih/FlatGov/pull/328) ([ayeshamk](https://github.com/ayeshamk))
- Docs/celery update [\#325](https://github.com/aih/FlatGov/pull/325) ([aih](https://github.com/aih))
- Add Cosponsor relations to Bill model [\#320](https://github.com/aih/FlatGov/pull/320) ([aih](https://github.com/aih))
- Add committee leadership positions [\#317](https://github.com/aih/FlatGov/pull/317) ([aih](https://github.com/aih))
- Clean up fields in detail view [\#312](https://github.com/aih/FlatGov/pull/312) ([aih](https://github.com/aih))
- Update billdata [\#311](https://github.com/aih/FlatGov/pull/311) ([aih](https://github.com/aih))
- Update billdata [\#310](https://github.com/aih/FlatGov/pull/310) ([aih](https://github.com/aih))
- Bug/type abbrev [\#308](https://github.com/aih/FlatGov/pull/308) ([aih](https://github.com/aih))
- Fix for type abbrev. Closes \#304 [\#307](https://github.com/aih/FlatGov/pull/307) ([aih](https://github.com/aih))
- Feature/related bills ayesha [\#302](https://github.com/aih/FlatGov/pull/302) ([ayeshamk](https://github.com/ayeshamk))
- Feature/bill committee [\#301](https://github.com/aih/FlatGov/pull/301) ([aih](https://github.com/aih))
- Fix for \#272 [\#299](https://github.com/aih/FlatGov/pull/299) ([aih](https://github.com/aih))
- Feature/cosponsor UI [\#297](https://github.com/aih/FlatGov/pull/297) ([aih](https://github.com/aih))
- Feature/cosponsor info [\#296](https://github.com/aih/FlatGov/pull/296) ([aih](https://github.com/aih))
- Feature/crec celery [\#295](https://github.com/aih/FlatGov/pull/295) ([aih](https://github.com/aih))
- Bump django from 3.1.6 to 3.1.8 [\#294](https://github.com/aih/FlatGov/pull/294) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump django from 3.1.6 to 3.1.8 in /server\_py [\#293](https://github.com/aih/FlatGov/pull/293) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bill short titles [\#292](https://github.com/aih/FlatGov/pull/292) ([aih](https://github.com/aih))
- Convert congress to ordinals [\#291](https://github.com/aih/FlatGov/pull/291) ([aih](https://github.com/aih))
- Bump urllib3 from 1.26.3 to 1.26.4 in /server\_py [\#288](https://github.com/aih/FlatGov/pull/288) ([dependabot[bot]](https://github.com/apps/dependabot))
- search bar UI updated [\#287](https://github.com/aih/FlatGov/pull/287) ([aih](https://github.com/aih))
- Feature/read bill ayesha [\#286](https://github.com/aih/FlatGov/pull/286) ([aih](https://github.com/aih))
- Add date templates [\#284](https://github.com/aih/FlatGov/pull/284) ([aih](https://github.com/aih))
- Press statements ayesha [\#282](https://github.com/aih/FlatGov/pull/282) ([ayeshamk](https://github.com/ayeshamk))
- Feature/crec celery [\#279](https://github.com/aih/FlatGov/pull/279) ([kapphire](https://github.com/kapphire))
- Feature/readme celery [\#278](https://github.com/aih/FlatGov/pull/278) ([aih](https://github.com/aih))
- Feature/readme celery [\#277](https://github.com/aih/FlatGov/pull/277) ([aih](https://github.com/aih))
- Feature/django scrapy [\#276](https://github.com/aih/FlatGov/pull/276) ([kapphire](https://github.com/kapphire))

## [v0.2.1](https://github.com/aih/FlatGov/tree/v0.2.1) (2021-03-30)

[Full Changelog](https://github.com/aih/FlatGov/compare/v0.2.0...v0.2.1)

**Implemented enhancements:**

- Combine tabs for Related and Similar Bills [\#243](https://github.com/aih/FlatGov/issues/243)
- Combine 'Related bills' with 'Similar bills' tables. Display the relevant columns for each [\#223](https://github.com/aih/FlatGov/issues/223)
- Combine scrapy`requirements.txt` into `server_py/requirements.txt` [\#211](https://github.com/aih/FlatGov/issues/211)
- Create a tab called 'Sections' in the Analyze Bills section that shows a section-by-section table [\#154](https://github.com/aih/FlatGov/issues/154)
- Integrate logic from this repo as a PR for govtrack [\#25](https://github.com/aih/FlatGov/issues/25)

**Fixed bugs:**

- Fix 'Number of sections matched': deduplicate [\#124](https://github.com/aih/FlatGov/issues/124)

**Closed issues:**

- Separate out the search bars [\#253](https://github.com/aih/FlatGov/issues/253)
- Populate Committees and Sponsors table with live data [\#252](https://github.com/aih/FlatGov/issues/252)
- Show 'No data available' if and only if there's no data [\#250](https://github.com/aih/FlatGov/issues/250)
- Bill summary: truncate and style [\#236](https://github.com/aih/FlatGov/issues/236)
- Change Biden SAP Scraper frequency to scrape daily [\#226](https://github.com/aih/FlatGov/issues/226)
- Got an error running load\_biden\_statements [\#225](https://github.com/aih/FlatGov/issues/225)
- Change the display formatting of the bills to "H.R. XXX" [\#221](https://github.com/aih/FlatGov/issues/221)
- Add Bill Map icon in the navigation  [\#220](https://github.com/aih/FlatGov/issues/220)
- Change the title on homepage to "Bill Map" and add description  [\#219](https://github.com/aih/FlatGov/issues/219)
- Change default font to Public Sans [\#218](https://github.com/aih/FlatGov/issues/218)
- Add tabs to the "Bills Related to \_\_\_\_\_\_\_\_\_" section [\#217](https://github.com/aih/FlatGov/issues/217)
- Have the "View full list of sponsors" button scroll down the page to "Sponsors of Related Measure"  [\#216](https://github.com/aih/FlatGov/issues/216)
- Remove "Read Bill:" from Overview section [\#215](https://github.com/aih/FlatGov/issues/215)
- Add actual bill summary instead of hard-coded text [\#214](https://github.com/aih/FlatGov/issues/214)
- Modify Committee documents scraper [\#204](https://github.com/aih/FlatGov/issues/204)
- Re-apply the related bills and analyze similar bills tabs from `main` to `feature/ui-enhance-ayesha-ah2` [\#197](https://github.com/aih/FlatGov/issues/197)
- Add congress and remove text of link in Statements tab [\#196](https://github.com/aih/FlatGov/issues/196)
- Re-apply the CBO tab data to detail.html [\#194](https://github.com/aih/FlatGov/issues/194)
- Re-apply the CRS reports UI to detail.html in `/feature/ui-enhance-ayesha-ah2` [\#193](https://github.com/aih/FlatGov/issues/193)
- Display committee documents on the bill corresponding to `associated_legislation` [\#192](https://github.com/aih/FlatGov/issues/192)
- Committee report has wrong 'billnumber' [\#191](https://github.com/aih/FlatGov/issues/191)
- Develop the Relevant Committee Documents section - Database, Back-end and UI development [\#180](https://github.com/aih/FlatGov/issues/180)
- Scrape data for Relevant Committee Documents section [\#179](https://github.com/aih/FlatGov/issues/179)
- CRS report: remove empty links [\#177](https://github.com/aih/FlatGov/issues/177)
- CRS reports: do not create a bill number if it does not exist-- just remove it from the list [\#174](https://github.com/aih/FlatGov/issues/174)
- Error loading SOA data -- field too short [\#168](https://github.com/aih/FlatGov/issues/168)
- Handle elasticsearch crashing on server [\#167](https://github.com/aih/FlatGov/issues/167)
- UI Sprint 1 \_ Sponsors Section Heading Change [\#165](https://github.com/aih/FlatGov/issues/165)
- UI Sprint 1 \_ Ad Space [\#162](https://github.com/aih/FlatGov/issues/162)
- Deduplicate es\_similarity by section [\#158](https://github.com/aih/FlatGov/issues/158)
- Back-end and UI development for CBO Score Section [\#156](https://github.com/aih/FlatGov/issues/156)
- Make CRS-to-bill associations using the metadata summary [\#148](https://github.com/aih/FlatGov/issues/148)
- Change title of sponsor section from "Sponsor" to "Sponsors of Related Measures"  [\#146](https://github.com/aih/FlatGov/issues/146)
- On FT\_branch\_1, for SAP, normalize date format and/or deduplicate data [\#138](https://github.com/aih/FlatGov/issues/138)
- Create Statement of Administrative Policy section on Bills page - UI Changes [\#132](https://github.com/aih/FlatGov/issues/132)
- Search bar should have filter for Congress session \(ex: 116th, 115th, 114th etc.\) [\#111](https://github.com/aih/FlatGov/issues/111)
- Calculate the length of matched sections for the bill-to-bill page [\#104](https://github.com/aih/FlatGov/issues/104)
- Understand the Context - Place tabs in correct order [\#103](https://github.com/aih/FlatGov/issues/103)
- Add a block for ads between section and related bills section  [\#99](https://github.com/aih/FlatGov/issues/99)
- Change section title to Bills Related to \[Bill Number\] [\#92](https://github.com/aih/FlatGov/issues/92)
- Show which 'similar' bills are also in the 'related' bills table [\#86](https://github.com/aih/FlatGov/issues/86)
- Add tabs for Analyze Related Bills section [\#84](https://github.com/aih/FlatGov/issues/84)
- Add version number to app, show in top right [\#76](https://github.com/aih/FlatGov/issues/76)
- Compare results from 'related bills' to 'similar bills' [\#70](https://github.com/aih/FlatGov/issues/70)
- Not all related bills are being added to the database [\#56](https://github.com/aih/FlatGov/issues/56)
- Scrape data for CBO report and relate to bill [\#52](https://github.com/aih/FlatGov/issues/52)
- Add scraper for CRS reports [\#51](https://github.com/aih/FlatGov/issues/51)
- Add section number to section header in similar bills display table, where available [\#41](https://github.com/aih/FlatGov/issues/41)
- Build scraper for Statements of Administrative Policy, connect to bill [\#34](https://github.com/aih/FlatGov/issues/34)
- Missing some related bills files [\#30](https://github.com/aih/FlatGov/issues/30)
- Interesting example: 115hr5164 [\#20](https://github.com/aih/FlatGov/issues/20)
- Mark titles with an indicator of whether they are for the whole bill or just a portion [\#17](https://github.com/aih/FlatGov/issues/17)

**Merged pull requests:**

- Reformat bill number for search [\#269](https://github.com/aih/FlatGov/pull/269) ([aih](https://github.com/aih))
- Feature/committee document ayesha [\#266](https://github.com/aih/FlatGov/pull/266) ([ayeshamk](https://github.com/ayeshamk))
- Bump pyyaml from 5.3.1 to 5.4 in /server\_py [\#262](https://github.com/aih/FlatGov/pull/262) ([dependabot[bot]](https://github.com/apps/dependabot))
- Feature/searchby congress 111 [\#261](https://github.com/aih/FlatGov/pull/261) ([aih](https://github.com/aih))
- Basic sponsor display is live. Issue \#252 [\#258](https://github.com/aih/FlatGov/pull/258) ([aih](https://github.com/aih))
- Feature/related similar bills [\#246](https://github.com/aih/FlatGov/pull/246) ([aih](https://github.com/aih))
- Feature/UI enhancements ayesha [\#244](https://github.com/aih/FlatGov/pull/244) ([ayeshamk](https://github.com/ayeshamk))
- Bump lxml from 4.6.2 to 4.6.3 in /scrapers [\#242](https://github.com/aih/FlatGov/pull/242) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump lxml from 4.6.2 to 4.6.3 [\#241](https://github.com/aih/FlatGov/pull/241) ([dependabot[bot]](https://github.com/apps/dependabot))
- Feature/related similar bills [\#239](https://github.com/aih/FlatGov/pull/239) ([aih](https://github.com/aih))
- Feature/221 billnumber format [\#238](https://github.com/aih/FlatGov/pull/238) ([aih](https://github.com/aih))
- Fix styling for bill summary [\#237](https://github.com/aih/FlatGov/pull/237) ([aih](https://github.com/aih))
- bill summary added [\#235](https://github.com/aih/FlatGov/pull/235) ([aih](https://github.com/aih))
- Bump urllib3 from 1.26.2 to 1.26.3 in /server\_py [\#234](https://github.com/aih/FlatGov/pull/234) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump django from 3.1 to 3.1.6 [\#233](https://github.com/aih/FlatGov/pull/233) ([dependabot[bot]](https://github.com/apps/dependabot))
- UI Changes [\#229](https://github.com/aih/FlatGov/pull/229) ([ayeshamk](https://github.com/ayeshamk))
- Feature/sap biden ayesha [\#222](https://github.com/aih/FlatGov/pull/222) ([ayeshamk](https://github.com/ayeshamk))
- Feature/committee doc main [\#202](https://github.com/aih/FlatGov/pull/202) ([ayeshamk](https://github.com/ayeshamk))
- Feature/UI enhance ayesha ah2 [\#199](https://github.com/aih/FlatGov/pull/199) ([ayeshamk](https://github.com/ayeshamk))
- Fix billnumber regex to allow 4 digit bills [\#187](https://github.com/aih/FlatGov/pull/187) ([aih](https://github.com/aih))
- Feature/cbo cherry pick [\#183](https://github.com/aih/FlatGov/pull/183) ([aih](https://github.com/aih))
- Add full bill indexing option [\#182](https://github.com/aih/FlatGov/pull/182) ([aih](https://github.com/aih))
- Feature/clean crs [\#176](https://github.com/aih/FlatGov/pull/176) ([aih](https://github.com/aih))
- Feature/issue 51 crs [\#171](https://github.com/aih/FlatGov/pull/171) ([aih](https://github.com/aih))
- Feature/soa ayesha ah [\#170](https://github.com/aih/FlatGov/pull/170) ([aih](https://github.com/aih))
- Feature/improve docs [\#169](https://github.com/aih/FlatGov/pull/169) ([aih](https://github.com/aih))
- Bug/add billupatejob [\#160](https://github.com/aih/FlatGov/pull/160) ([aih](https://github.com/aih))
- Feature/clean similar [\#159](https://github.com/aih/FlatGov/pull/159) ([aih](https://github.com/aih))
- Feature/similarity pre [\#157](https://github.com/aih/FlatGov/pull/157) ([aih](https://github.com/aih))
- Feature/149 similarity improve [\#153](https://github.com/aih/FlatGov/pull/153) ([aih](https://github.com/aih))

## [v0.2.0](https://github.com/aih/FlatGov/tree/v0.2.0) (2021-02-05)

[Full Changelog](https://github.com/aih/FlatGov/compare/v0.1.1-billdata...v0.2.0)

**Implemented enhancements:**

- Filter similar bills to return only bills with a best score \> threshold [\#127](https://github.com/aih/FlatGov/issues/127)
- Set up bill xml data on Flatgov server [\#116](https://github.com/aih/FlatGov/issues/116)
- List matches from different bill versions in bill-to-bill [\#112](https://github.com/aih/FlatGov/issues/112)
- Default table pagination size to 100 [\#68](https://github.com/aih/FlatGov/issues/68)

**Fixed bugs:**

- Fix routing for pdfs for SAPs [\#139](https://github.com/aih/FlatGov/issues/139)
- Fix total score in bills page: deduplicate [\#125](https://github.com/aih/FlatGov/issues/125)

**Closed issues:**

- In the `bill_similarity` function, find the latest version of a bill to process [\#144](https://github.com/aih/FlatGov/issues/144)
- Update the elastic\_load task to delete a bill \(including version number\) before indexing [\#140](https://github.com/aih/FlatGov/issues/140)
- Error for 116hr1 on FT\_branch\_1: 'permanent\_pdf\_link' attribute has no file associated with it [\#137](https://github.com/aih/FlatGov/issues/137)
- Increase default  bill similarity query results to 20  [\#134](https://github.com/aih/FlatGov/issues/134)
- Create tables on Database from Trump Administration's Data [\#133](https://github.com/aih/FlatGov/issues/133)
- Scrape Statement of Administrative Policies of Trump Administration [\#131](https://github.com/aih/FlatGov/issues/131)
- Problem running migrations [\#121](https://github.com/aih/FlatGov/issues/121)
- Advanced Search should fit the size of the entire width of the search bar on the top [\#117](https://github.com/aih/FlatGov/issues/117)
- Allow user to select bill with a number less than 4 digits [\#115](https://github.com/aih/FlatGov/issues/115)
- Prepare deployment of application \(with cron job to scrape and process bills\) [\#113](https://github.com/aih/FlatGov/issues/113)
- In bill page, similarity table, sort by top score [\#107](https://github.com/aih/FlatGov/issues/107)
- Filter out duplicate section matches in bill-to-bill [\#106](https://github.com/aih/FlatGov/issues/106)
- Show the number of matched sections on the bill-to-bill page [\#105](https://github.com/aih/FlatGov/issues/105)
- Understand the Context - Statement of Administration Policy \(SOA\) [\#97](https://github.com/aih/FlatGov/issues/97)
- Change sponsors section title to "Sponsors of Related Measures" [\#95](https://github.com/aih/FlatGov/issues/95)
- Create a bill scraper and update mechanism to deploy and update similar bills [\#87](https://github.com/aih/FlatGov/issues/87)
- Add a bill-to-bill detail page [\#85](https://github.com/aih/FlatGov/issues/85)
- Scrape Trump Statement of Administration Policy before change in administration  [\#82](https://github.com/aih/FlatGov/issues/82)
- For the 'Analyze Bills' table, list the total number of sections in the bill at the top [\#75](https://github.com/aih/FlatGov/issues/75)
- Default order 'Analyze similar bills' by score [\#71](https://github.com/aih/FlatGov/issues/71)
- Add columns to bill similarity table: bill title, number of sections matched, best match score, best match sections [\#69](https://github.com/aih/FlatGov/issues/69)
- Long content in tables should be viewable on hover \(alt text?\)  [\#66](https://github.com/aih/FlatGov/issues/66)
- Tables should allow resizing of columns [\#65](https://github.com/aih/FlatGov/issues/65)
- The weekly calendar should begin on Monday instead of Sunday [\#59](https://github.com/aih/FlatGov/issues/59)
- Measure bill similarity using the ES sections index [\#58](https://github.com/aih/FlatGov/issues/58)
- Error running python manage.py migrate [\#49](https://github.com/aih/FlatGov/issues/49)
- Error running python manage.py bill\_data [\#48](https://github.com/aih/FlatGov/issues/48)
- Use model data to display in the `bills` view, for the related bills and sponsors tables [\#47](https://github.com/aih/FlatGov/issues/47)
- Save related bills information \(from scripts/relatedBills.py\) to the database  [\#46](https://github.com/aih/FlatGov/issues/46)
- Create model for related bills [\#45](https://github.com/aih/FlatGov/issues/45)
- Create a 'bill' model [\#44](https://github.com/aih/FlatGov/issues/44)

**Merged pull requests:**

- bill version added to elastic search and bill similarity [\#149](https://github.com/aih/FlatGov/pull/149) ([aih](https://github.com/aih))
- Bug/issue 124 125 [\#143](https://github.com/aih/FlatGov/pull/143) ([aih](https://github.com/aih))
- Uniquely index bill documents [\#142](https://github.com/aih/FlatGov/pull/142) ([aih](https://github.com/aih))
- Update scraping docs [\#136](https://github.com/aih/FlatGov/pull/136) ([aih](https://github.com/aih))
- Feature/deployment [\#135](https://github.com/aih/FlatGov/pull/135) ([aih](https://github.com/aih))
- Issue/82 statements admin policy [\#130](https://github.com/aih/FlatGov/pull/130) ([aih](https://github.com/aih))
- Bump lxml from 4.6.1 to 4.6.2 in /server\_py [\#129](https://github.com/aih/FlatGov/pull/129) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump lxml from 4.6.1 to 4.6.2 [\#128](https://github.com/aih/FlatGov/pull/128) ([dependabot[bot]](https://github.com/apps/dependabot))
- Issue/version number [\#126](https://github.com/aih/FlatGov/pull/126) ([aih](https://github.com/aih))
- Issue/autocomplete [\#122](https://github.com/aih/FlatGov/pull/122) ([aih](https://github.com/aih))
- Issue/105 107 [\#114](https://github.com/aih/FlatGov/pull/114) ([kapphire](https://github.com/kapphire))
- bill to bill page completed [\#88](https://github.com/aih/FlatGov/pull/88) ([kapphire](https://github.com/kapphire))
- Issue/69 bill similarity [\#77](https://github.com/aih/FlatGov/pull/77) ([kapphire](https://github.com/kapphire))
- Add columns to bill similarity table: bill title, number of sections … [\#74](https://github.com/aih/FlatGov/pull/74) ([aih](https://github.com/aih))
- Feature/bill sponsor [\#73](https://github.com/aih/FlatGov/pull/73) ([aih](https://github.com/aih))
- Round similarity score [\#72](https://github.com/aih/FlatGov/pull/72) ([aih](https://github.com/aih))
- Feature/bill sponsor [\#67](https://github.com/aih/FlatGov/pull/67) ([kapphire](https://github.com/kapphire))
- Feature/bill sponsor [\#57](https://github.com/aih/FlatGov/pull/57) ([kapphire](https://github.com/kapphire))

## [v0.1.1-billdata](https://github.com/aih/FlatGov/tree/v0.1.1-billdata) (2020-11-03)

[Full Changelog](https://github.com/aih/FlatGov/compare/e09abd141f928b9c1a053107a6782deadfda378a...v0.1.1-billdata)

**Implemented enhancements:**

- Add num to header in similar bills list, where available [\#42](https://github.com/aih/FlatGov/issues/42)
- Link bill number in tables [\#40](https://github.com/aih/FlatGov/issues/40)
- Create a json file for each bill that lists metadata including related bills [\#23](https://github.com/aih/FlatGov/issues/23)
- Display sponsors of related bills [\#21](https://github.com/aih/FlatGov/issues/21)
- Add shared sponsors to relatedBills [\#14](https://github.com/aih/FlatGov/issues/14)
- In relatedBills, add items for relationships identified in related\_bills of data.json [\#12](https://github.com/aih/FlatGov/issues/12)
- Add titles that differ by year in a `titles_year` field [\#9](https://github.com/aih/FlatGov/issues/9)
- Create enriched relatedBills JSON [\#7](https://github.com/aih/FlatGov/issues/7)

**Fixed bugs:**

- Error when missing sponsor state or district [\#26](https://github.com/aih/FlatGov/issues/26)

**Closed issues:**

- Check bills in 116hr5150 for related bills [\#32](https://github.com/aih/FlatGov/issues/32)
- Create home page [\#19](https://github.com/aih/FlatGov/issues/19)
- Re-style tabular table to match UX  [\#18](https://github.com/aih/FlatGov/issues/18)
- Integrate relatedBills info into Django app [\#15](https://github.com/aih/FlatGov/issues/15)
- Duplicate bill being added in related bills [\#10](https://github.com/aih/FlatGov/issues/10)
- Create a relatedBills.json for same\_titles [\#6](https://github.com/aih/FlatGov/issues/6)
- relatedBills.py [\#4](https://github.com/aih/FlatGov/issues/4)
- Readme Changes [\#3](https://github.com/aih/FlatGov/issues/3)

**Merged pull requests:**

- Similarity [\#39](https://github.com/aih/FlatGov/pull/39) ([aih](https://github.com/aih))
- Ui similar [\#37](https://github.com/aih/FlatGov/pull/37) ([aih](https://github.com/aih))
- Elastic [\#36](https://github.com/aih/FlatGov/pull/36) ([aih](https://github.com/aih))
- Home page [\#33](https://github.com/aih/FlatGov/pull/33) ([zomdar](https://github.com/zomdar))
- Fix for \#26 [\#29](https://github.com/aih/FlatGov/pull/29) ([aih](https://github.com/aih))
- Deploy [\#28](https://github.com/aih/FlatGov/pull/28) ([aih](https://github.com/aih))
- Home page [\#27](https://github.com/aih/FlatGov/pull/27) ([aih](https://github.com/aih))
- Calculate a data file of related files for each bill [\#22](https://github.com/aih/FlatGov/pull/22) ([aih](https://github.com/aih))
- Show relatedbills in Django app. \#15 [\#16](https://github.com/aih/FlatGov/pull/16) ([aih](https://github.com/aih))
- Add GPO related bills. \#12 [\#13](https://github.com/aih/FlatGov/pull/13) ([aih](https://github.com/aih))
- Create a related bills json with same and similar title bills \#9 and \#10 [\#11](https://github.com/aih/FlatGov/pull/11) ([aih](https://github.com/aih))
- Enriched relatedBills JSON [\#8](https://github.com/aih/FlatGov/pull/8) ([adamwjo](https://github.com/adamwjo))
- Adambranch [\#5](https://github.com/aih/FlatGov/pull/5) ([adamwjo](https://github.com/adamwjo))
- Adam's Sandbox [\#2](https://github.com/aih/FlatGov/pull/2) ([adamwjo](https://github.com/adamwjo))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
