import os
import sys
import RFEM.dependencies # dependency check ahead of imports
import socket
import requests
from suds.client import Client
from RFEM.enums import ObjectTypes, ModelType, AddOn
from RFEM.suds_requests import RequestsTransport
from suds.cache import DocumentCache
from tempfile import gettempdir
import time

# Connect to server
# Check server port range set in "Program Options & Settings"
# By default range is set between 8081 ... 8089
print('Connecting to server...')

# local machine url format: 'http://127.0.0.1'
url = 'http://127.0.0.1'
# port format: '8081'
port = '8081'
urlAndPort = url+':'+port

# Check if port is listening
a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

location = (url[7:], int(port))
result_of_check = a_socket.connect_ex(location)

if result_of_check == 0:
    a_socket.close()
else:
    print('Error: Port '+urlAndPort+' is not open.')
    print('Please check:')
    print('- If you have started RFEM application at the remote destination correctly.')
    a_socket.close()
    sys.exit()

# Delete cached WSDL older than 1 day to reflect newer version of RFEM
cacheLoc = os.path.join(gettempdir(), 'WSDL')
currentTime = time.time()
if os.path.exists(cacheLoc):
    for file in os.listdir(cacheLoc):
        filePath = os.path.join(cacheLoc, file)
        if (currentTime - os.path.getmtime(filePath)) > 86400:
            os.remove(filePath)

# Check for issues locally and remotely
try:
    ca = DocumentCache(location=cacheLoc)
    client = Client(urlAndPort+'/wsdl', location = urlAndPort, cache=ca)
except:
    print('Error: Connection to server failed!')
    print('Please check:')
    print('- If you have started RFEM application')
    print('- If all RFEM dialogs are closed')
    print('- If server port range is set correctly')
    print('- If you have a valid Web Services license')
    print('- Check Program Options & Settings > Web Services')
    print('On remote PC please check:')
    print('- If the firewall enables you to listen to selected port.')
    sys.exit()

try:
    modelLst = client.service.get_model_list()
except:
    print('Error: Please check if all RFEM dialogs are closed.')
    input('Press Enter to exit...')
    sys.exit()

# Persistent connection
# 'session' and 'trans'(port) enable Client to work within 1 session which is much faster to execute.
# Without it the session lasts only one request which results in poor performance.
# Assigning session to application Client (here client) instead of model Client
# results also in poor performance.

class Model():
    clientModel = None
    clientModelDct = {}

    def __init__(self,
                 new_model: bool=True,
                 model_name: str="TestModel.rf6",
                 delete: bool=False,
                 delete_all: bool=False):
        """
        Class object representing individual model in RFEM.
        Class enables to edit multiple models in one session through holding
        one transport session active by not setting 'trans' into Client.

        Args:
            new_model (bool, optional): Set to True if new model is requested.
            model_name (str, optional): Defaults to "TestModel".
            delete (bool, optional):  Delete results
            delete_all (bool, optional): Delete all objects in Model.
        """

        cModel = None
        modelLst = []
        modelVct = client.service.get_model_list()
        if modelVct:
            modelLst = modelVct.name

        # The model suffix is omitted in modelLs, so it must be omitted in model_name to match exactly
        original_model_name = model_name
        if '.' in model_name:
            model_name = model_name.split('.')[0]

        if new_model:
            # Requested new model but the model with given name was already connected
            if model_name in self.clientModelDct:
                cModel = self.clientModelDct[model_name]
                cModel.service.delete_all_results()
                cModel.service.delete_all()

            # Requested new model, model with given name DOESN'T exist yet
            else:
                modelPath = ''
                # Requested new model, model with given name was NOT connected yet but file with the same name was opened
                if model_name in modelLst:
                    id = 0
                    for i,j in enumerate(modelLst):
                        if modelLst[i] == model_name:
                            id = i
                    modelPath =  client.service.get_model(id)
                else:
                    modelPath =  client.service.new_model(original_model_name)
                modelPort = modelPath[-5:-1]
                modelUrlPort = url+':'+modelPort
                modelCompletePath = modelUrlPort+'/wsdl'

                session = requests.Session()
                adapter = requests.adapters.HTTPAdapter(pool_connections=1, pool_maxsize=1)
                session.mount('http://', adapter)
                trans = RequestsTransport(session)

                cModel = Client(modelCompletePath, transport=trans, location = modelUrlPort, cache=ca, timeout=360)

                self.clientModelDct[model_name] = cModel

        else:
            # Requested model which was already connected
            assert model_name in self.clientModelDct or model_name in modelLst, 'WARNING: '+model_name +' is not connected neither opened in RFEM.'

            if model_name in self.clientModelDct:
                cModel = self.clientModelDct[model_name]
            elif model_name in modelLst:
                id = 0
                for i,j in enumerate(modelLst):
                    if modelLst[i] == model_name:
                        id = i
                modelPath =  client.service.get_model(id)
                modelPort = modelPath[-5:-1]
                modelUrlPort = url+':'+modelPort
                modelCompletePath = modelUrlPort+'/wsdl'

                session = requests.Session()
                adapter = requests.adapters.HTTPAdapter(pool_connections=1, pool_maxsize=1)
                session.mount('http://', adapter)
                trans = RequestsTransport(session)

                cModel = Client(modelCompletePath, transport=trans, location = modelUrlPort, cache=ca, timeout=360)

                self.clientModelDct[model_name] = cModel
            else:
                print('Model name "'+model_name+'" is not created in RFEM. Consider changing new_model parameter in Model class from False to True.')
                sys.exit()

        if delete:
            print('Deleting results...')
            cModel.service.delete_all_results()
        if delete_all:
            print('Delete all...')
            cModel.service.delete_all()

        # when using multiple instances/model
        self.clientModel = cModel
        # when using only one instance/model
        Model.clientModel = cModel

    def __delete__(self, index_or_name):
        '''
        Purpose of this function is to facilitate removing client instances
        from clientModelDct dictionary, which is held in Model for the purpose of
        working with multiple models either created directly in RFEM or opened from file.

        Args:
            index_or_name (str or int): Name of the index of model
        '''
        if isinstance(index_or_name, str):
            self.clientModelDct.pop(index_or_name)
            if len(self.clientModelDct) > 0:
                model_key = list(self.clientModelDct)[-1]
                self.clientModel = self.clientModelDct[model_key]
            else:
                self.clientModel = None
        if isinstance(index_or_name, int):
            assert index_or_name <= len(self.clientModelDct)
            modelLs = client.service.get_model_list()

            if modelLs:
                self.clientModelDct.pop(modelLs.name[index_or_name])
                if len(self.clientModelDct) > 0:
                    model_key = list(self.clientModelDct)[-1]
                    self.clientModel = self.clientModelDct[model_key]
                else:
                    self.clientModel = None

def clearAttributes(obj):
    '''
    Clears object attributes.
    Sets all attributes to None.
    Use it whenever you create new (sub)object.

    Args:
        obj: object to clear
    '''

    # iterator
    it = iter(obj)
    for i in it:
        obj[i[0]] = None

    return obj

def deleteEmptyAttributes(obj):
    '''
    Delete all attributes that are None for better performance.

    Args:
        obj: object to clear
    '''
    it = [] # iterator
    try:
        it = iter(obj)
    except:
        ValueError('WARNING: Object feeded to deleteEmptyAttributes function is not iterable. It is type: '+str(type(obj)+'.'))

    for i in it:
        if isinstance(i, str) or isinstance(i, int) or isinstance(i, float) or isinstance(i, bool):
            continue
        if len(i) > 2:
            i = deleteEmptyAttributes(i)
        elif i[1] is None or i[1] == "":
            delattr(obj, i[0])
        elif isinstance(i[1], str) or isinstance(i[1], int) or isinstance(i[1], float) or isinstance(i[1], bool):
            pass
        else:
            if isinstance(i, tuple):
                i = list(i)
                i[1] = deleteEmptyAttributes(i[1])
                i = tuple(i)
            else:
                i[1] = deleteEmptyAttributes(i[1])

    return obj

def openFile(model_path):
    '''
    Open file with a name.
    This routine primarily adds client instance into
    Model.clientModelLst which manages all connections to the models.
    New Model class instance is invoked.
    It should be used when opening a file.

    Args:
        model_path (str): Path to RFEM6 model.
    Returns:
        model (client instance): RFEM model instance
    '''
    assert os.path.exists(model_path)

    file_name = os.path.basename(model_path)
    client.service.open_model(model_path)
    return Model(True, file_name)

def closeModel(index_or_name, save_changes = False):
    '''
    Close any model connected to client with index or name.
    Make sure to close the first open model last.
    First model carries whole session (locking of the RFEM).

    Args:
        index_or_name : Model Index or Name to be Close
        save_changes (bool): Enable/Disable Save Changes Option
    '''
    if isinstance(index_or_name, int):
        Model.__delete__(Model, index_or_name)
        client.service.close_model(index_or_name, save_changes)

    elif isinstance(index_or_name, str):
        if '.rf6' in index_or_name:
            index_or_name = index_or_name[:-4]

        modelLs = client.service.get_model_list().name
        Model.__delete__(Model, index_or_name)
        client.service.close_model(modelLs.index(index_or_name), save_changes)
    else:
        assert False, 'Parameter index_or_name must be int or string.'

def closeAllModels(save_changes = False):
    '''
    Function that closes all opened models in reverse order.

    Args:
        save_changes (bool): Enable/Disable Save Changes Option
    '''
    modelLs = client.service.get_model_list().name
    for j in reversed(modelLs):
        closeModel(j, save_changes)

def saveFile(model_path):
    '''
    This function saves a model in a .rf6 file.

    Args:
        index_or_name : Model Index or Name to be Close
        model_path: Path to RFEM6 model.
    '''
    if model_path[len(model_path) - 4:len(model_path)].lower() != '.rf6':
        model_path = model_path + '.rf6'

    Model.clientModel.service.save(model_path)

def insertSpaces(lst: list):
    '''
    Add spaces between list of numbers.
    Returns list of values.
    '''
    return ' '.join(str(item) for item in lst)

def Calculate_all(generateXmlSolverInput: bool = False, model = Model):
    '''
    Calculates model.
    CAUTION: Don't use it in unit tests!
    It works when executing tests individually but when running all of them
    it causes RFEM to stuck and generates failures, which are hard to investigate.

    Args:
        generateXmlSolverInput (bool): Generate XML Solver Input
        model (RFEM Class, optional): Model to be edited
    '''
    calculationMessages = model.clientModel.service.calculate_all(generateXmlSolverInput)
    return calculationMessages

def ConvertToDlString(s):
    '''
    The function converts strings commonly used in RFEM so that they
    can be used In WebServices. It solved issue #4.
    Examples:
    '1,3'       -> '1 3'
    '1, 3'      -> '1 3'
    '1-3'       -> '1 2 3'
    '1,3,5-9'   -> '1 3 5 6 7 8 9'

    Args:
        s (str): RFEM Common String

    Returns a WS conform string.
    '''

    # Parameter is not of required type.
    assert isinstance(s, (list, str))

    if isinstance(s, list):
        return ' '.join(map(str, s))

    s = s.strip()
    s = s.replace(',', ' ')
    s = s.replace('  ', ' ')
    lst = s.split(' ')
    new_lst = []
    for element in lst:
        if '-' in element:
            inLst = element.split('-')
            start = int(inLst[0])
            end   = int(inLst[1])
            inLst = []
            for i in range(start, end + 1):
                inLst.append(str(i))

            inS = ' '.join(inLst)
            new_lst.append(inS)
        else:
            new_lst.append(element)

    return ' '.join(new_lst)

def ConvertStrToListOfInt(st):
    """
    This function coverts string to list of integers.
    Args:
        st (str): RFEM Common String
    """
    st = ConvertToDlString(st)
    lstInt = []
    while st:
        intNumber = 0
        if ' ' in st:
            idx = st.index(' ')
            intNumber = int(st[:idx])
            st = st[idx+1:]
        else:
            intNumber = int(st)
            st = ''
        lstInt.append(intNumber)
    return lstInt

def CheckIfMethodOrTypeExists(modelClient, method_or_type, unitTestMode=False):
    """
    Check if SOAP method or type is present in your version of RFEM.
    Use it only in your examples.
    Unit tests except msg from SUDS where this is checked already.

    Args:
        modelClient (Model.clientModel)
        method_or_type (str): Method or Type of SOAP Client
        unitTestMode (bool): Unit Test Mode

    Returns:
        bool: Status of method or type.

    Note:
        To get list of methods invoke:
        list_of_methods = [method for method in Model.clientModel.wsdl.services[0].ports[0]]
    """
    assert modelClient, "WARNING: modelClient is not initialized."

    if method_or_type not in str(modelClient):
        if unitTestMode:
            return True
        else:
            assert False, "WARNING: Used method/type: %s is not implemented in Web Services yet." % (method_or_type)

    return not unitTestMode


def GetAddonStatus(modelClient, addOn = AddOn.stress_analysis_active):
    """
    Check if Add-on is reachable and active.
    For some types of objects, specific Add-ons need to be enabled.

    Args:
        modelClient (Model.clientModel)
        addOn (enum): AddOn Enumeration

    Returns:
        (bool): Status of Add-on
    """
    if modelClient is None:
        print("WARNING: modelClient is not initialized.")
        return False

    addons = modelClient.service.get_addon_statuses()
    dct = {}
    for lstType in addons:
        if not isinstance(lstType[1], bool) and len(lstType[1]) > 1:
            addon = [lst for lst in lstType[1]]
            for item in addon:
                dct[str(item[0])] = bool(item[1])
        elif isinstance(lstType[1], bool):
            dct[str(lstType[0])] = bool(lstType[1])
        else:
            assert False

    # sanity check
    assert addOn.name in dct, f"WARNING: {addOn.name} Add-on can not be reached."

    return dct[addOn.name]

def SetAddonStatus(modelClient, addOn = AddOn.stress_analysis_active, status = True):
    """
    Activate or deactivate Add-on.
    For some types of objects, specific Add-ons need to be enabled.

    Args:
        modelClient (Model.clientModel)
        addOn (enum): AddOn Enumeration
        status (bool): in/active

    Analysis addOns list:
        material_nonlinear_analysis_active
        structure_stability_active
        construction_stages_active
        time_dependent_active
        influence_lines_areas_active
        form_finding_active
        cutting_patterns_active
        torsional_warping_active
        cost_estimation_active

    Design addOns list:
        stress_analysis_active
        concrete_design_active
        steel_design_active
        timber_design_active
        aluminum_design_active
        steel_joints_active
        timber_joints_active
        craneway_design_active

    Dynamic addOns list:
        modal_active
        equivalent_lateral_forces_active
        spectral_active
        time_history_active
        pushover_active
        harmonic_response_active

    Special aadOns list:
        building_model_active
        wind_simulation_active
        tower_wizard_active
        tower_equipment_wizard_active
        piping_active
        air_cushions_active
        geotechnical_analysis_active
    """

    # this will also provide sanity check
    currentStatus = GetAddonStatus(modelClient, addOn)
    if currentStatus != status:
        addonLst = modelClient.service.get_addon_statuses()
        if addOn.name in addonLst['__keylist__']:
            addonLst[addOn.name] = status
        else:
            for listType in addonLst['__keylist__']:
                if not isinstance(addonLst[listType], bool) and addOn.name in addonLst[listType]:
                    addonLst[listType][addOn.name] = status

        modelClient.service.set_addon_statuses(addonLst)

def CalculateSelectedCases(loadCases: list = None, designSituations: list = None, loadCombinations: list = None,skipWarnings = True, model = Model):
    '''
    This method calculate just selected objects - load cases, designSituations, loadCombinations

    Args:
        loadCases (list, optional): Load Case List
        designSituations (list, optional): Design Situations List
        loadCombinations (list, optional): Load Combinations List
        model (RFEM Class, optional): Model to be edited
    '''
    specificObjectsToCalculate = model.clientModel.factory.create('ns0:calculate_specific_loadings')
    if loadCases:
        for loadCase in loadCases:
            specificObjectsToCalculateLS = model.clientModel.factory.create('ns0:calculate_specific_loadings.loading')
            specificObjectsToCalculateLS.no = loadCase
            specificObjectsToCalculateLS.type = ObjectTypes.E_OBJECT_TYPE_LOAD_CASE.name
            specificObjectsToCalculate.loading.append(specificObjectsToCalculateLS)

    if designSituations:
        for designSituation in designSituations:
            specificObjectsToCalculateDS = model.clientModel.factory.create('ns0:calculate_specific_loadings.loading')
            specificObjectsToCalculateDS.no = designSituation
            specificObjectsToCalculateDS.type = ObjectTypes.E_OBJECT_TYPE_DESIGN_SITUATION.name
            specificObjectsToCalculate.loading.append(specificObjectsToCalculateDS)


    if loadCombinations:
        for loadCombination in loadCombinations:
            specificObjectsToCalculateCC = model.clientModel.factory.create('ns0:calculate_specific_loadings.loading')
            specificObjectsToCalculateCC.no = loadCombination
            specificObjectsToCalculateCC.type = ObjectTypes.E_OBJECT_TYPE_LOAD_COMBINATION.name
            specificObjectsToCalculate.loading.append(specificObjectsToCalculateCC)
    try:
        calculationMessages = model.clientModel.service.calculate_specific(specificObjectsToCalculate,skipWarnings)
    except Exception as inst:
        calculationMessages = "Calculation was unsuccessful: " + inst.fault.faultstring

    return calculationMessages

def FirstFreeIdNumber(memType = ObjectTypes.E_OBJECT_TYPE_MEMBER, parent_no: int = 0, model = Model):
    '''
    This method returns the next available Id Number for the selected object type

    Args:
        memType (enum): Object Type Enumeration
        parent_no (int): Object Parent Number
            Note:
            (1) A geometric object has, in general, a parent_no = 0
            (2) The parent_no parameter becomes significant for example with loads
        model (RFEM Class, optional): Model to be edited
    '''
    return model.clientModel.service.get_first_free_number(memType.name, parent_no)

def SetModelType(model_type = ModelType.E_MODEL_TYPE_3D, model = Model):
    '''
    This method sets the model type. The model type is E_MODEL_TYPE_3D by default.

    Args:
        model_type (enum): Modal Type Enumeration. The available model types are listed below.
            ModelType.E_MODEL_TYPE_1D_X_3D
            ModelType.E_MODEL_TYPE_1D_X_AXIAL
            ModelType.E_MODEL_TYPE_2D_XY_3D
            ModelType.E_MODEL_TYPE_2D_XY_PLATE
            ModelType.E_MODEL_TYPE_2D_XZ_3D
            ModelType.E_MODEL_TYPE_2D_XZ_PLANE_STRAIN
            ModelType.E_MODEL_TYPE_2D_XZ_PLANE_STRESS
            ModelType.E_MODEL_TYPE_3D
        model (RFEM Class, optional): Model to be edited
    '''

    model.clientModel.service.set_model_type(model_type.name)

def GetModelType(model = Model):
    '''
    The method returns a string of the current model type.

    Args:
        model (RFEM Class): Model Instance
    '''

    return model.clientModel.service.get_model_type()

def NewModelAsCopy(old_model_name: str = '',
                   old_model_folder: str = ''):
    '''
    The method creates a new model as copy from an existing model

    Args:
        old_model_name (str): Old Model Name
        old_model_folder (str): Old Model Folder
    '''

    # Old Model Name
    new_model_name = ''
    if '.rf6' in old_model_name:
        new_model_name = old_model_name[:-4] + '_copy'

    else:
         assert TypeError('Model ' + old_model_name +  ' does not exist')

    old_model_path = os.path.join(old_model_folder, old_model_name)

    # New Model Name
    newModelAsCopy = client.service.new_model_as_copy(new_model_name, old_model_path)

    return newModelAsCopy

def GetModelMainParameters(model = Model):
    '''
    The method returns the main parameters of the current model.

    Args:
        model (RFEM Class, optional): Model to be edited
    '''

    # Client Model | Get Model Main Parameters
    return model.clientModel.service.get_model_main_parameters()

def GetModelId(model = Model):
    '''
    This method returns model id as a string.

    Args:
        model (RFEM Class, optional): Model to be edited
    '''

    # Client Model | Get Model ID
    return model.clientModel.service.get_model_main_parameters().model_id

def GetModelParameters(model = Model):
    '''
    This method retuns the parameters of the current model.

    Args:
        model (RFEM Class, optional): Model to be edited
    '''

    # Client Model | Get Model Parameters
    return model.clientModel.service.get_model_parameters()

def GetModelSessionId(model = Model):
    '''
    This method returns model session id as a string.

    Args:
        model (RFEM Class, optional): Model to be edited
    '''

    # Client Model | Get Session Id
    return model.clientModel.service.get_session_id()

def GetName():
    '''
    This method returns app name as a string.
    '''

    # Client Application | Get Information
    return client.service.get_information().name

def GetVersion():
    '''
    This method returns version as a string.
    '''

    # Client Application | Get Information
    return client.service.get_information().version

def GetLanguage():
    '''
    This method returns language as a string.
    '''

    # Client Application | Get Information
    return client.service.get_information().language_name

def GetAppSessionId():
    '''
    This method returns session id as a string.
    '''

    # Client Application | Get Session ID
    return client.service.get_session_id()

def getPathToRunningRFEM():
    '''
    Find the path to the directory where RFEM is currently running.
    This is helpful when using server version, because it can't process relative paths.
    '''
    import psutil
    rstab9 = False
    rstab9Server = False
    path = ''

    for p in psutil.process_iter(['name', 'exe']):
        if p.info['name'] == 'RFEM6.exe':
            idx = p.info['exe'].find('bin')
            path = p.info['exe'][:idx]
        elif p.info['name'] == 'RFEM6Server.exe':
            idx = p.info['exe'].find('bin')
            path = p.info['exe'][:idx]
        elif p.info['name'] == 'RSTAB9.exe':
            rstab9 = True
        elif p.info['name'] == 'RSTAB9Server.exe':
            rstab9Server = True

    if rstab9 or rstab9Server:
        raise ValueError('Careful! You are running RFEM Python Client on RSTAB.')
    if not path:
        raise ValueError('Is it possible that RFEM is not runnnning?')

    return path
