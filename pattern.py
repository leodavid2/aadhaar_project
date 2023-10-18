import re


class find_pattern:
      
      @staticmethod
      def find_aadhaar_numbers(data):
            aadhaar_pattern = re.compile(r"(\d{4} \d{4} \d{4})")
            aadhaar_numbers = re.findall(aadhaar_pattern, data)
            return aadhaar_numbers[0]
      
      @staticmethod
      def find_dob(data):
            dob_pattern = re.compile(r"DOB\D*(\d{1,2}/\d{1,2}/\d{4})")
            dobs = re.findall(dob_pattern, data)
            return str(dobs[0])
      
      @staticmethod
      def find_addresses(data):
            
            starting_point = r"(?:Address:|Address :)"
            ending_point_pattern = r"\b\d{6}\b"
            address_pattern = rf"{starting_point}\s*(.*?{ending_point_pattern})"
            matches = re.findall(address_pattern, data, re.DOTALL)
            for match in matches:
                  # unnecessary_words = [ 'Ve', 'ard ot get', 'EN OF OG,', 'HH WT,', 'Tam,', 'Wal:', 've' ,'HATO PROT','TAN,','sede,','Wal:','-10, poor och, daft Vs, GR, BST',
                              
                  #                   '4a','Wet feat,','feet,','ve','Gon@ 5 Cus)','GOEG ISG','(psCui PHASE 1,','CeuevG, WNsuGuy, WpsuGus,','AGeucnes7, SMM HG,','CHT T Guero 1']
      
                  # patterns = '|'.join(map(re.escape, unnecessary_words))

                  # cleaned_data = re.sub(patterns, '', match, flags=re.IGNORECASE).strip()

                  # cleaned_data = re.sub(r'\s+', ' ', cleaned_data).strip()

                  return match
            return match
      
      @staticmethod
      def extract_name_from_data(data):
            name_pattern = r"[A-Z][a-z]+(?: [A-Z][a-z]+)*(?: [A-Z][a-z]+)?"
            pattern = r"(.*)(?=DOB\s*:\s*\d{1,2}/\d{1,2}/\d{2,4})"
            matches = re.findall(pattern, data, re.DOTALL)
            extracted_names = []
            for match in matches:
                  names = re.findall(name_pattern, match)
                  extracted_names.extend(names)

            if len(extracted_names[-1]) < 6:
                  extracted_names.pop()

            return extracted_names[-1]
      
      @staticmethod
      def find_gender_patterns(data):
            pattern = r'\b(?:MALE|Male|male|FEMALE|Female|female)\b'
            matches = re.findall(pattern, data)
            print("matchs :",matches)

            for match in matches:
                  return match

            return match
      
      
