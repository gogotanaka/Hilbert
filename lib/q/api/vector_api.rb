module Q
  module API
    module VectorApi
      def execute(nums)
        "c(#{nums.join(', ')})"
      end
      module_function :execute
    end
  end
end
