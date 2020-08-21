def walkBillDirs(rootDir = '../congress/data', processFile = logName, dirMatch = getTopBillLevel, fileMatch = isDataJson):
    for dirName, subdirList, fileList in os.walk(rootDir):
      if dirMatch(dirName):
        logger.info('Entering directory: %s' % dirName)
        #need help here, whats fitem go fitem
        filteredFileList = [fitem for fitem in fileList if fileMatch(fitem)]
        for fname in filteredFileList:
        #process file takes in logName() by default but in Main you are using addToBillsMeta()?
        # Is it this way because you anticipate more than one processfile method? 
            processFile(dirName=dirName, fileName=fname)


def addToBillsMeta(dirName: str, fileName: str):
    #what does load json do?
    billDict = loadJSON(os.path.join(dirName, fileName))
    billCongressTypeNumber = getBillCongressTypeNumber(billDict)
    if not billCongressTypeNumber:
      return
    if not billsMeta.get(billCongressTypeNumber):
      billsMeta[billCongressTypeNumber] = {}
    titles = getBillTitles(billDict)
    billsMeta[billCongressTypeNumber]['titles'] = [title.get('title') for title in titles]
    billsMeta[billCongressTypeNumber]['titles_whole_bill'] = [title.get('title') for title in titles if not title.get('is_for_portion')]
    billsMeta[billCongressTypeNumber]['cosponsors'] = getCosponsors(fileDict=billDict, includeFields=['name', 'bioguide_id'])
    billCount = len(billsMeta.keys()) 
    if billCount % SAVE_ON_COUNT == 0:
      saveBillsMeta(billsMeta)

def getBillCongressTypeNumber(fileDict: Dict):
  bill_id = fileDict.get('bill_id')
  if bill_id:
    bill_id_parts = bill_id.split('-')
    return bill_id_parts[1] + bill_id_parts[0]
  else:
    logging.error('No bill_id: ' + str(fileDict.get('bill_type')))
    return None




