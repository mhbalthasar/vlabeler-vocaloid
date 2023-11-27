let wavFolderName = params['wavFolderName']
let wavFolder = root.resolve(wavFolderName);
let modules = []
let wavFiles = wavFolder.listChildFiles().filter(f => f.getExtension() === 'wav')
//模板创建器
wavFiles.forEach(wavFile => {
    let wavName = wavFile.getNameWithoutExtension()
    let transFile = wavFolder.resolve(wavName + '.trans')
    let vLabelFile = wavFolder.resolve(wavName + '.vlab')
    if (transFile.exists()) {
        let lines = transFile.readLines().map(l => l.trim())
        let i = 1
        let tiers = []
        while (i < lines.length) {
            let line = lines[i]
            let index = i - 1
            let name=""
            if (line.startsWith("[")) {
                name=line.substring(1,line.indexOf("]"))
                if(line.indexOf("]")<line.length-1)
                {
                    name = name + "##" + line.substring(line.indexOf("]")+1,line.length)
                }
            }
            if (name.length>0) {
                tiers.push({index, name})
            }
            i++
        }
        
        for (let tier of tiers) {
            let moduleName = wavFile.getName() + " ["+tier.name + '] _' + tier.index
            let len_phn=tier.name.split(' ').length;
            let sampleNames=[];
            let asNames=[];
            console.log(moduleName);
            if(len_phn==3)
            {
                let prt1=tier.name.split(' ')[0]+' '+tier.name.split(' ')[1];
                let prt2=tier.name.split(' ')[1]+' '+tier.name.split(' ')[2];

                moduleName = wavFile.getName() + " [(" + prt1 + ')] ' + tier.name.split(' ')[2]+ '] _' + tier.index
                let asFileName = wavFolder.resolve(wavName + '.vlab' + tier.index+"_1")
                let sampleName = wavFile.getName()
                sampleNames=[sampleName];
                asNames=[asFileName.getAbsolutePath()];
                let module = new ModuleDefinition(
                    moduleName,//Name
                    wavFolder.getAbsolutePath(),//SampleDirPath
                    sampleNames,//SampleFileNames
                    asNames,//inputFilePathesvLabelFile.getAbsolutePath()
                    asFileName.getAbsolutePath()//labelFilePathes
                )
                modules.push(module)
                
                moduleName = wavFile.getName() + " ["  + tier.name.split(' ')[0] + " (" + prt2 + ')] _' + tier.index
                asFileName = wavFolder.resolve(wavName + '.vlab' + tier.index+"_2")
                sampleNames=[sampleName];
                asNames=[asFileName.getAbsolutePath()];
                module = new ModuleDefinition(
                    moduleName,//Name
                    wavFolder.getAbsolutePath(),//SampleDirPath
                    sampleNames,//SampleFileNames
                    asNames,//inputFilePathesvLabelFile.getAbsolutePath()
                    asFileName.getAbsolutePath()//labelFilePathes
                )
                modules.push(module)
            }else
            {
                let asFileName = wavFolder.resolve(wavName + '.vlab' + tier.index)
                let sampleName = wavFile.getName()
                sampleNames=[sampleName];
                asNames=[asFileName.getAbsolutePath()];
                let module = new ModuleDefinition(
                    moduleName,//Name
                    wavFolder.getAbsolutePath(),//SampleDirPath
                    sampleNames,//SampleFileNames
                    asNames,//inputFilePathesvLabelFile.getAbsolutePath()
                    asFileName.getAbsolutePath()//labelFilePathes
                )
                modules.push(module)
            }
        }
    }
})
